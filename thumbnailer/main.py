import json
import requests
import base64

from io import BytesIO

from flask import make_response
import os
from imagethumbnailer import resizeImage
import pdfhumbnailer
from config import conf
import utils




def main(request):
	conf["hmackey"]=bytes(str(os.environ['HMACKEY']), 'utf-8')
	data = request.get_json()

	res=[]
	if not utils.hmacVerify(data["dataStr"].encode("ASCII"), data["sign"]):
		return make_response({"error":"HMAC Key not match"})
	data = json.loads(base64.b64decode(data["dataStr"].encode("ASCII")).decode("UTF-8"))

	url = data["url"]
	#We must append only if local dev server
	baseUrl = data["baseUrl"]
	if not str(url).startswith("https://"):
		url=baseUrl+url

	response = requests.get(url, allow_redirects=False)
	while response.status_code > 300 and response.status_code < 400:  # We must follow the redirect
		url = response.headers['Location']
		response = requests.get(url, allow_redirects=False)

	if response.headers['content-type'].split("/")[0]=="image":

		for i, sizeDict in enumerate(data["params"]):
			if "sites" in sizeDict:
				#raise Exception("")
				return make_response({"error": "Error we have and derive for PDF's"})
			if "resolution" in sizeDict:
				#raise Exception("Error we have and derive for PDF's")
				return make_response({"error": "Error we have and derive for PDF's"})

			image,name = resizeImage(response.content,sizeDict)

			if data["nameOnly"]:
				outData = BytesIO()
				image.save(outData, sizeDict.get("fileExtension", "webp"))
				outSize = outData.tell()
				res.append({"name": name, "size": outSize})

			else:
				res.append(uploadImage(image, data, name, sizeDict, i))


	elif response.headers['content-type']=="application/pdf":


		pdfhumbnailer.savepdf(response.content)
		siteCount=pdfhumbnailer.countSites()



		for i, sizeDict in enumerate(data["params"]):

			if "sites" in sizeDict:
				pages = pdfhumbnailer.getsiteNumbers(sizeDict.get("sites", ""),siteCount)
			else:
				pages=[str(p) for p in range(1,siteCount+1)]
			id = pdfhumbnailer.pdftoImages(sizeDict, pages)
			for count,page in enumerate(pages):
				try:
					with open("/tmp/" + id + "-%s.jpg" % str(count+1), "rb") as f:
						image = f.read()
				except Exception as e:
					print("---Error---")
					print(e)
					continue

				image,  name = resizeImage(image, sizeDict, name="site-%s" % page,fromPDF=True)

				customdata={}
				if "resolution" in sizeDict:
					customdata["resolution"]=sizeDict["resolution"]

				if data["nameOnly"]:
					res.append({"name": name,"mimeType": sizeDict.get("mimeType", "image/webp")})

				else:
					res.append(uploadImage(image, data, name, sizeDict, i, customdata))





	return make_response({"values":res})





def uploadImage(image:object,data:dict,fileName:str,sizeDict:dict,index:int,customData:dict=None)->dict:

	"""
		A fuction to Upload the Images to the Cloud Storage.
		First the function gets the Uploadurl form the Server (data["baseUrl"]). After that
		it sends the Binary image data to the UploadUrl (Cloud Storage)

		:param image: PIL Image
		:param data: The data dict that we get from the server it stores:skeys,authData,authSig,targetKey
		:param fileName: Filename for the Image
		:param sizeDict: Dictonary for the MimeType and fileExtension
		:param index: index of the skey and so on. (data["skey"][index])
		:param customData: Data that we store in our _customData dict. If a key in customData is set that we have in
			_customData it overrides it.

		:return:  dict
	"""
	width, height = image.size

	fileExtension = sizeDict.get("fileExtension", "webp")
	mimeType = sizeDict.get("mimeType", "image/webp")

	outData = BytesIO()
	image.save(outData, fileExtension)
	outData.seek(0)
	upload_response = requests.post(data["uploadUrls"][data["targetKey"]+fileName], data=outData)
	uploadData = upload_response.json()

	name = fileName
	_customData={
				"height": height,
				"width": width,
				"mimetype": uploadData["contentType"],
			}
	if customData is not None:
		for key,value in customData.items():
			_customData[key]=value
	return{
		name: {
			"size": int(uploadData["size"]),
			"mimetype": uploadData["contentType"],
			"customData": _customData
		}
	}
