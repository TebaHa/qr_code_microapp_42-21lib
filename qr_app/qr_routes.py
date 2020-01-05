# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    qr_routes.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: zytrams <zytrams@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/11/08 21:37:59 by zytrams           #+#    #+#              #
#    Updated: 2020/01/05 05:08:46 by zytrams          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from qr_app import qr_app
from os import environ as Env
from qr_app.qr_composer import QrComposer
from qr_app.qr_image import QrImage
from flask import send_file
import json
import os
import requests as Reqst

qr_compo = QrComposer(3, 8)

# QR_CODE -> потом ссылка простым текстом под qrcode потом название книги
def get_url():
	if Env.get('URL'):
		url = 'http://' + Env.get('URL')
	if Env.get('URL_IP') and Env.get('URL_PORT') and Env.get('URL_ROUTE'):
		url = 'http://' + Env.get('URL_IP') + ':' + Env.get('URL_PORT') + Env.get('URL_ROUTE')
	else:
		url = 'http://42lib.site'
	return url

@qr_app.route('/')
def index():
	return "ВЫ КТО ТАКИЕ?!! Я ВАС НЕ ЗВАЛ!!! ИДИТЕ ***!!!"

@qr_app.route('/api/get/all')
def get_qrs_all():
	url = get_url() + '/api/get_all_books'
	books = json.loads(Reqst.get(url).content)
	qr_books = []
	for book in books:
		#qr_app.logger.info()
		qr_books.append(QrImage('http://42lib.site/book' + book['id'], book['name']))
	qr_compo.put_qrs(qr_books)
	try:
		return send_file(os.path.dirname(os.path.realpath(__file__)) + '/../libqrcodes.pdf', attachment_filename='libqrcodes.pdf')
	except Exception as e:
		return str(e)

@qr_app.route('/book<int:b_id>')
def get_qr(b_id):
	url = get_url()
	Reqst.get(url)
	return str(b_id)
