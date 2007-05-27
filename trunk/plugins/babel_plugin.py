#$ neutron_plugin 01
# -*- coding: koi8-r -*-
import babelizer
import russian
import re

_sub_charrefs = re.compile(r'&#(\d+|x[\da-e]+);', re.I).sub        
def _repl_charrefs(m):
    g = m.group(1)
    if g[0]=='x':
        c = int(g[1:], 16)
    else:
        c = int(g)
    try:
        return unichr(c)
    except ValueError:
        return m.group() # or return '?'


def decode_charrefs(text, coding):
    text = text.decode(coding, 'replace')
    return _sub_charrefs(_repl_charrefs, text)

def handler_babel_babel(type, source, parameters):
	splitdata = string.split(parameters)
	if len(splitdata) >= 3:
		from_lang = splitdata[0]
		to_lang = splitdata[1]
		body = string.join(splitdata[2:])
		try:
			reply = babelizer.translate(body, from_lang, to_lang)
		except babelizer.LanguageNotAvailableError:
			reply = 'Invalid Language'
		except babelizer.BabelfishChangedError:
			print str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
			reply = 'Unknown Error'
	else:
		reply = 'Syntax Error'
	if not reply:
		reply = 'No Results'
	reply = unicode(reply, 'utf-8')
	smsg(type, source, reply)

def handler_babel_tre(type, source, parameters):
	handler_babel_babel(type, source, u'russian english ' + parameters)

def handler_babel_translate(type, source, parameters):
	splitdata = string.split(parameters)
	if len(splitdata) >= 3:
		from_lang = splitdata[0]
		to_lang = splitdata[1]
		body = string.join(splitdata[2:])
		try:
			reply = russian.translate(body, from_lang, to_lang)
# modified by Guest007 at 29.05.2006			
		except russian.LanguageNotAvailableError, instance:
			reply = 'Invalid Language -> ' + instance.value + ", check 'help !translate'"
# end of modificaton (29.05.2006)			
		except russian.BabelfishChangedError:
			print str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
			reply = 'Unknown Error'
	else:
		reply = 'Syntax Error'
	if not reply:
		reply = 'No Results'
# Added by Guest007

        reply = decode_charrefs(reply, "utf-8")

#end of addition
	smsg(type, source, reply)

def handler_babel_enru(type, source, parameters):
	handler_babel_translate(type, source, u'e r ' + parameters)

def handler_babel_esru(type, source, parameters):
	handler_babel_translate(type, source, u's r ' + parameters)

def handler_babel_babelize(type, source, parameters):
	splitdata = string.split(parameters)
	if len(splitdata) >= 3:
		from_lang = splitdata[0]
		through_lang = splitdata[1]
		body = string.join(splitdata[2:])
		try:
			results = babelizer.babelize(body, from_lang, through_lang)
			reply = ''
			for result in results:
				reply += '\n' + result
		except babelizer.LanguageNotAvailableError:
			reply = 'Invalid Language'
		except babelizer.BabelfishChangedError:
			print str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
			reply = 'Unknown Error'
	else:
		reply = 'Syntax Error'
	if not reply:
		reply = 'No Results'
	smsg(type, source, reply)

def handler_babel_esperanto(type, source, parameters):
	formdata = 'al=2&de=3&al-k=4&teksto=' + urllib.quote(parameters)
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('lingvo.org', 80))
	s.send("""POST /cgi-bin/eoxx/eoxx HTTP/1.1
User-Agent: Mozilla/5.0 (compatible; Konqueror/3; Linux 2.4.18)
Pragma: no-cache
Cache-control: no-cache
Accept: text/*, image/jpeg, image/png, image/*, */*
Accept-Encoding: x-gzip, gzip, identity
Accept-Charset: ISO-8859-1, utf-8;q=0.5, *;q=0.5
Accept-Language: en, POSIX
Host: lingvo.org
Content-Type: application/x-www-form-urlencoded
Content-Length: """ + str(len(formdata)) + '\n\n' + formdata + '\n\n')
	pagedata = s.recv(1024)
	s.close()
	#formdata = urllib.urlencode({'al': '2', 'de': '3', 'al-k': '4', 'teksto': parameters})
	#f = urllib.urlopen('http://lingvo.org/cgi-bin/eoxx/eoxx', formdata)
	#pagedata = f.read()
	#print pagedata
	try:
		reply = string.split(string.split(pagedata, 'lang="en">')[1], '</font>')[0].strip()
	except:
		reply = 'Unknown Error'
	smsg(type, source, reply)

def handler_mueller(type, source, parameters):
	parameters =  parameters.replace(';',' ')
        parameters =  parameters.replace('~',' ')
        parameters =  parameters.replace('!',' ')
        parameters =  parameters.replace('@',' ')
        parameters =  parameters.replace('#',' ')
        parameters =  parameters.replace('$',' ')
        parameters =  parameters.replace('%',' ')
        parameters =  parameters.replace('^',' ')
        parameters =  parameters.replace('&',' ')
        parameters =  parameters.replace('*',' ')
        parameters =  parameters.replace('(',' ')
        parameters =  parameters.replace(')',' ')
        parameters =  parameters.replace('[',' ')
        parameters =  parameters.replace(']',' ')
        parameters =  parameters.replace('{',' ')
        parameters =  parameters.replace('}',' ')
        parameters =  parameters.replace(':',' ')
	pipe = os.popen('mova -d Mueller7accentGPL.koi -W  ' + parameters)
	return_value = pipe.read(1024)
	reply = decode_charrefs(return_value, 'koi8-r')
	smsg(type, source, reply)

register_command_handler(handler_mueller, '!mueller', 0, 'Translates a word from english to russian using local mueller dictionary', '!mueller <word>', ['!mueller word'])

register_command_handler(handler_mueller, '!m', 0, 'Translates a word from english to russian using local mueller dictionary', '!m <word>', ['!m word'])

register_command_handler(handler_babel_babel, '!babel', 0, 'Translate a phrase from one language to another using AltaVista BabelFish.', '!babel <fromlang> <tolang> <phrase>', ['!babel english spanish hello', '!babel fr en bonjour'])

register_command_handler(handler_babel_translate, '!translate', 0, 'Translate a phrase from one language to another using translate.ru.', '!translate <fromlang> <tolang> <phrase>', ['!translate e s hello', '!translate f e bonjour'])

# examples: 
register_command_handler(handler_babel_tre, '!tre', 0, 'Translate a phrase from Russian to English (shortcut).', '!tre <phrase>', ['!tre ????????'])

register_command_handler(handler_babel_enru, '!enru', 0, 'Translate a phrase from English to Russian (shortcut).', '!enru <phrase>', ['!enru the tortoise'])
register_command_handler(handler_babel_enru, '!esru', 0, 'Translate a phrase from Spanish to Russian (shortcut).', '!esru <phrase>', ['!esru corazon'])

# register_command_handler(handler_babel_esperanto, '!esperanto', 0, 'Translate a phrase from Esperanto to English.', '!esperanto <phrase>', ['!esperanto Saluton!'])

register_command_handler(handler_babel_babelize, '!babelize', 0, 'Translate a phrase back and forth from one language to another (gives interesting results).', '!babelize <fromlang> <throughlang> <phrase>', ['!babelize english spanish hello'])

