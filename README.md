# lcsh_to_lcgft
Python 3 script to replace certain LCSHs used as genre/form headings with LCGFT equivalents

# What you need
1. Python 3
2. pymarc
3. List that include LCSHs and their LCGFT equivalents and URIs (example: replace.csv)
4. MARC file

# Background
At our library, appx. 4,460 LCSHs are used as genre/form headings in our records, of which 496 LCSHs can be replaced with their LCGFT equivalents. For example,
| LCSH                                      | LCGFT                                    | LCGFT URI                                             |
|------------------------------------------ | ---------------------------------------- | ----------------------------------------------------- |
| Dissertations, Academic.                  | Academic theses                          | http://id.loc.gov/authorities/genreForms/gf2014026039 |
| Account books.                            | Account books                            | http://id.loc.gov/authorities/genreForms/gf2017026136 |
| Action and adventure films.               | Action and adventure films               | http://id.loc.gov/authorities/genreForms/gf2011026005 |
| Adventure films.                          | Action and adventure films               | http://id.loc.gov/authorities/genreForms/gf2011026005 |
| Action films.                             | Action and adventure films               | http://id.loc.gov/authorities/genreForms/gf2011026005 |
| Action and adventure television programs. | Action and adventure television programs | http://id.loc.gov/authorities/genreForms/gf2011026006 |
| Adventure television programs.            | Action and adventure television programs | http://id.loc.gov/authorities/genreForms/gf2011026006 |
| Administrative regulations.               | Administrative regulations               | http://id.loc.gov/authorities/genreForms/gf2011026030 |
| Aerial views.                             | Aerial views                             | http://id.loc.gov/authorities/genreForms/gf2011026033 |

Now that LCGFT is our primary thesaurus for genre/form headings, using this script, we update a 655 field like this.
from:  655  \0 $a Dissertations, Academic.
to:    655  \7 $a Academic theses. $2 lcgft $0 http://id.loc.gov/authorities/genreForms/gf2014026039

Note: If the LCSH doesn't have LCGFT equivalent, we leave it as is.
