import sys
from tagger.interrogator import Interrogator, WaifuDiffusionInterrogator
from PIL import Image
from pathlib import Path
import argparse
import requests

from tagger.interrogators import interrogators

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--dir', help='ディレクトリ内の画像すべてに予測を行う')
group.add_argument('--file', help='ファイルに対して予測を行う')

parser.add_argument(
    '--threshold',
    type=float,
    default=0.35,
    help='予測値の足切り確率（デフォルトは0.35）')
parser.add_argument(
    '--ext',
    default='.txt',
    help='dirの場合にキャプションファイルにつける拡張子')
parser.add_argument(
    '--model',
    default='wd14-convnextv2.v1',
    choices=list(interrogators.keys()),
    help='予測に使用するモデル名')

args = parser.parse_args()

# charger le model
interrogator = interrogators[args.model]

def image_interrogate(image_path: Path):
    """
    画像パスから予測を行う
    """
    im = Image.open(image_path)
    result = interrogator.interrogate(im)
    return Interrogator.postprocess_tags(result[1], threshold=args.threshold)

from flask import Flask, jsonify, request

app = Flask(__name__)

# SERVER HTTP
@app.route('/eval', methods=['GET'])
def get_tasks():
    file_name = request.values.get("file") 
    tags = image_interrogate(Path(file_name))
    return jsonify({'tasks': tags})

if __name__ == '__main__':
    app.run(debug=True, port=1554)
    
