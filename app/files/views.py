from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.database import db
from app.settings import Config
from app.files.forms import UploadForm, SearchForm
from app.file_processing.tasks import process_file
from app.models.file import File, Pages, Sentences, Words, Statistics, Status

import json
import time
import os
from zipfile import ZipFile

file_views_blueprint = Blueprint('files',
                                 __name__,
                                 template_folder='templates'
                                 )


@file_views_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    upload_form = UploadForm()

    if upload_form.validate_on_submit():
        if upload_form.file.data:
            file = upload_form.file.data
            filename = secure_filename(file.filename)
            title = filename.split(".")[0]

        elif upload_form.text.data and upload_form.name.data:
            filename = secure_filename(upload_form.name.data + ".txt")
            title = upload_form.name.data

        path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), filename)
        duplicate_count = 0

        while os.path.exists(path):
            duplicate_count += 1
            new_title = f"{title}-{duplicate_count}"
            filename = f"{new_title}.txt"
            path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), filename)

        if duplicate_count is not 0:
            title = new_title

        os.makedirs(os.path.dirname(path), exist_ok=True)

        if upload_form.file.data:
            file.save(path)
        elif upload_form.text.data:
            with open(path, 'w', encoding="utf-8") as f:
                f.write(upload_form.text.data)

        file_model = File(title, current_user.id, filename)
        file_model.save()

        file_status = Status(file_model.id, lemmatized="lemat" in upload_form.processes.data, completed=False)
        file_status.save()

        process_file(file_model.id, current_user.id, filename, upload_form.processes.data)

        return "File is being processed"
    return render_template('upload.html', upload_form=upload_form)


@file_views_blueprint.route('/files', defaults={'page_num': 1}, methods=['GET', 'POST'])
@file_views_blueprint.route('/files/<int:page_num>', methods=['GET', 'POST'])
@login_required
def all_files(page_num):
    files = File.get_active_files(current_user.id).paginate(per_page=4, page=page_num)

    return render_template('files.html', block_files=files)


@file_views_blueprint.route('/files/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
@login_required
def concrete(file_id, page_id):

    file = File.file_by_id(file_id)
    page = file.pages[page_id - 1]
    statistics = Statistics.statistics_for_file(file_id)
    word_list = page.get_text()

    lemma_list = []

    for word in page.get_all_words().all():
        dict = {
            'lemma': word.lemma,
            'tags': word.pos_tags
        }

        lemma_list.append(dict)

    search_form = SearchForm()
    if search_form.validate_on_submit() and search_form.search_field.data:
        return redirect(url_for('files.search', file_id=file_id, search_word=search_form.search_field.data, page_num=1))

    return render_template('view_file.html', file=file, word_list=word_list, statistics=statistics,
                           search_form=search_form, lemma_list=json.dumps(lemma_list, ensure_ascii=False))


@file_views_blueprint.route('/files/<int:file_id>/search/<string:search_word>/<int:page_num>', methods=['GET', 'POST'])
@login_required
def search(search_word, file_id, page_num):

    search_results = Words.search_by_raw(file_id, search_word).group_by(Words.sentence_id).paginate(per_page=16,
                                                                                                    page=page_num)
    sentences = []

    file = File.file_by_id(file_id)

    for word in search_results.items:
        sentence_object = Sentences.query.get(word[1].id)
        sentence = {
            "raw_text": sentence_object.get_text(),
            "highlight": word[2].raw,
            "page_id": file.relative_page_by_id(sentence_object.page_id),
        }

        sentences.append(sentence)

    return render_template('details.html', file_id=file_id, sentences=sentences, paginate=search_results,
                           search_word=search_word)


@file_views_blueprint.route('/files/disable_file/<int:file_id>', methods=['GET', 'POST'])
@login_required
def disable_file(file_id):
    file = File.file_by_id(file_id)

    if current_user.id == file.user_id:
        file.disable()

    return redirect(request.referrer)


@file_views_blueprint.route('/files/download_file/<int:file_id>', methods=['GET', 'POST'])
@login_required
def download_file(file_id):
    file = File.file_by_id(file_id)
    file_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), file.title)
    absolute_path = os.path.join(current_app.root_path, "uploads", str(current_user.id))

    if current_user.id == file.user_id:
        with ZipFile(f"{file_path}.zip", 'w') as zipobj:
            zipobj.write(f"{file_path}.txt", f"{file.title}.txt")

            if file.status[0].lemmatized:
                file.create_json()
                zipobj.write(f"{file_path}-lemmatized.json", f"{file.title}-lemmatized.json")

        return send_from_directory(absolute_path, f"{file.title}.zip", as_attachment=True)

    return redirect(url_for('files.all_files'))
