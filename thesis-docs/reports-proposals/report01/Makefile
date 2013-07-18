FILES = proposal.aux proposal.blg proposal.dvi proposal.log proposal.ps proposal.pdf

proposal: proposal.tex proposal.bib
	dvipdf proposal.dvi
	dvips -o proposal.ps -t letter proposal.dvi

bbl:
	rm -rf proposal.bbl
	latex proposal
	bibtex proposal
	latex proposal
	latex proposal

clean:
	rm -f $(FILES)
