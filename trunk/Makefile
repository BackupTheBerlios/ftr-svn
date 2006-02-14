CP=cp
RM=rm
FORMATTER_HTML=rest2html
FORMATTER_HTML_OPTIONS=--embed-stylesheet --stylesheet-path /usr/share/python-docutils/stylesheets/default.css
H_VERSION = $(shell grep ^HUMAN frequent-task-reminder.py | awk -F \" '{print $$2}')
# "
BASENAME = frequent-task-reminder
VERNAME = $(BASENAME)_$(H_VERSION)

.PHONY: all dist clean doc

all:

clean:
	$(RM) -fR $(BASENAME)_*.*.*
	$(RM) *.pyc *.html ChangeLog.txt
	@echo So fresh and so clean!

docs:
	$(FORMATTER_HTML) $(FORMATTER_HTML_OPTIONS) README.txt > README.html

dist: all
	$(RM) -fR dist
	mkdir dist
	@# Copy all the interesting files.
	$(CP) *.txt *.py dist
	$(CP) ChangeLog.txt dist
	$(RM) dist/maintenance.txt
	@# Nice. Now package.
	$(RM) -fR $(VERNAME) $(VERNAME).tar.bz2
	mv dist $(VERNAME)
	arcdir -t tar.bz2 $(VERNAME)
	$(RM) -fR $(VERNAME)
	@echo Done!

dist-log: all
	$(RM) -fR dist
	mkdir dist
	@# Copy all the interesting files.
	$(CP) *.txt *.py dist
	@# Now generate a changes log.
	svn update
	svn log | fmt > ChangeLog.txt
	$(CP) ChangeLog.txt dist
	$(RM) dist/maintenance.txt
	@# Nice. Now package.
	$(RM) -fR $(VERNAME) $(VERNAME).tar.bz2
	mv dist $(VERNAME)
	arcdir -t tar.bz2 $(VERNAME)
	$(RM) -fR $(VERNAME)
	@echo Done!
        

#add_words:
#	cat source.en.txt |aspell list --lang=en |sort|uniq> tmp.txt
#	-cat source.en.txt.ignored_words >> tmp.txt
#	sort tmp.txt|uniq> source.en.txt.ignored_words
#	rm tmp.txt
#	svn diff source.en.txt.ignored_words
#	cat source.es.txt |aspell list --lang=es |sort|uniq> tmp.txt
#	-cat source.es.txt.ignored_words >> tmp.txt
#	sort tmp.txt|uniq> source.es.txt.ignored_words
#	rm tmp.txt
#	svn diff source.es.txt.ignored_words
#
#spell:
#	aspell --lang=en create master ./.aspell.dic.source.en.txt < ./source.en.txt.ignored_words
#	aspell check source.en.txt --lang=en --add-extra-dicts ./.aspell.dic.source.en.txt
#	aspell --lang=es create master ./.aspell.dic.source.es.txt < ./source.es.txt.ignored_words
#	aspell check source.es.txt --lang=es --add-extra-dicts ./.aspell.dic.source.es.txt
        
