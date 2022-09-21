import time
from io import BytesIO
from PIL import Image
from PIL import ImageCms

def resizeImage(content,sizeDict,name=None,fromPDF=False,nameOnly=False):

	imagefile = BytesIO(content)

	imagefile.seek(0)
	image = Image.open(imagefile)

	icc = image.info.get('icc_profile')
	if icc and not fromPDF: #TODO Warum brauchen wird das ?

		f = BytesIO(icc)
		src_profile = ImageCms.ImageCmsProfile(f)
		dst_profile = ImageCms.createProfile('sRGB')
		image = ImageCms.profileToProfile(image, inputProfile=src_profile, outputProfile=dst_profile, outputMode="RGB")



	fileExtension = sizeDict.get("fileExtension", "webp")

	if "width" in sizeDict and "height" in sizeDict:
		width = sizeDict["width"]
		height = sizeDict["height"]
		targetName = "thumbnail-%s-%s.%s" % (width, height, fileExtension)
	elif "width" in sizeDict:
		width = sizeDict["width"]
		height = int((float(image.size[1]) * float(width / float(image.size[0]))))
		targetName = "thumbnail-w%s.%s" % (width, fileExtension)
	else:  # No default fallback - ignore
		return None,None
	if not nameOnly:
		image = image.resize((width, height), Image.ANTIALIAS)
	if name is not None:
		targetName = name+"-"+targetName
	#res = uploadImage(image,data,targetName,sizeDict,fileExtension,i,width, height,res)
	return image,targetName
