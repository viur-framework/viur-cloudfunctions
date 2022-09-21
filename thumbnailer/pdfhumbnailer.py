import ghostscript
import utils
from io import BytesIO
import locale
from typing import List

def savepdf(content):
	with open("/tmp/input.pdf","wb") as f:
		f.write(content)

def pdftoImages(sizedict,pagelist=[]):

	id=utils.generateRandomString()
	resolution="200"
	if "resolution" in sizedict:
		resolution=sizedict.get("resolution")

	args = ["pdf2jpeg",  # actual value doesn't matter
			"-dNOPAUSE",
			"-sDEVICE=jpeg",
			"-sPageList="+",".join(pagelist),
			"-r"+resolution,
			"-sOutputFile=/tmp/"+id+"-%d.jpg",
			"/tmp/input.pdf"]


	ghostscript.Ghostscript(*args)
	return id

def countSites():
	"""
		Helper function that count the pages in the pdf
	"""
	args = [
		"pdfpagecount",
		"-dNOPAUSE",
		#"--permit-file-read=/tmp/", #if version >9.5
		"-c", '(/tmp/input.pdf) (r) file runpdfbegin pdfpagecount = quit'
	]

	encoding = locale.getpreferredencoding()
	args = [a.encode(encoding) for a in args]


	stdout = BytesIO()
	stderr = BytesIO()
	try:
		gs = ghostscript.Ghostscript(stdout=stdout,stderr=stderr,*args)
		gs.exit()

		output = str(stdout.getvalue(), encoding="utf-8").strip()
		output=output.split("\n")


	except Exception as e:
		print("err is")
		print(e)

	return int(output[-1]) #Last index is the page number


def getsiteNumbers(sites:str,sitecount:int)->List[str]:
	"""
		This helper function converts a string of sites in a list of sitenumbers
		.. Example: Giving the following function,
			>>> getsiteNumbers("1,2,3",6)
			>>>["1","2","3"]

			>>> getsiteNumbers("1,even",6)List
			>>>["1","2","4","6"]

			>>> getsiteNumbers("1-3,5-*",6)
			>>>["1","2","3","5","6"]

			>>> getsiteNumbers("4-6,*",6)
			>>>["1","2","3","4","5","6"]

		:param sites: string to convert
		:param sitecount: number of pages in the pdf

	"""
	sites = sites.split(",")
	sitenumbers = []
	for site in sites:
		if "-" not in site:
			if "even" == site:
				for i in range(1, sitecount):
					if i % 2 == 0 and i not in sitenumbers:
						sitenumbers.append(i)
			elif "odd" == site:
				for i in range(1, sitecount):
					if i % 2 == 1 and i not in sitenumbers:
						sitenumbers.append(i)
			elif "*" == site:
				for i in range(1, sitecount):
					if i not in sitenumbers:
						sitenumbers.append(i)

			elif site not in sitenumbers:
				sitenumbers.append(int(site))
		else:
			startsite, endsite = site.split("-")
			startsite = int(startsite)
			if endsite == "*":
				endsite = sitecount
			else:
				endsite = int(endsite)
			if startsite > endsite:
				raise ValueError("startsite>endsite")
			for i in range(startsite, endsite + 1):
				if i not in sitenumbers:
					sitenumbers.append(i)
	sitenumbers.sort()
	sitenumbers = [str(site) for site in sitenumbers]
	return sitenumbers
