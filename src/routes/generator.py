"""
Defines the blueprint for the generator
"""
from flask import Blueprint, request, send_file
from cookie.generator import *
import tempfile
import pathlib
import uuid

GENERATOR_BLUEPRINT = Blueprint("generator", __name__)


@GENERATOR_BLUEPRINT.post('/generator/cutter')
def generate():
    f = request.files['file']
    basepath = tempfile.gettempdir()
    image_ext = pathlib.Path(f.filename).suffix
    filename = uuid.uuid4().hex

    input_path = str(pathlib.Path(basepath, f"{filename}{image_ext}").absolute())
    f.save(input_path)

    _, mask = create_mask(input_path)
    _, max_contours = create_line_geometry(mask.copy())

    points = preprocess_line([[float(p[0][0]), float(p[0][1])] for p in max_contours])

    output_path = str(pathlib.Path(basepath, f"{filename}.stl").absolute())
    generate_stl(list(points.coords), output_path)

    try:
        return send_file(output_path, as_attachment=True, download_name=f.filename.strip(image_ext) + '.stl')
    except Exception as e:
        return str(e)