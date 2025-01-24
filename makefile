TARGET = cv

tex: 
	pdflatex -shell-escape $(TARGET).tex
	pdflatex -shell-escape $(TARGET).tex
	#mv $(TARGET).pdf ../$(TARGET).pdf

	rm *.aux *.log *.out &
	rm -r _minted* &
