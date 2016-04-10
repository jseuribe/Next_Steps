import unicodedata

def normalize_from_unicode(inp_str):
	unicode_vessel = unicodedata.normalize('NFKD', inp_str).encode('ascii', 'ignore')
	return unicode_vessel
