# H-2 Debarment and Violations Analysis

This repository contains data, code, and methodologies supporting the May 12, 2016 BuzzFeed News article, "[The Pushovers](https://www.buzzfeed.com/kenbensinger/the-pushovers)."

- [Data](#data)
- [Analyses](#analyses)
- [Feedback](#feedback)

## Data

The analyses presented below depend on three datasets. Each is based on data or records from the Department of Labor, the agency responsible for protecting workers and vetting employers seeking visas:

- The Wage and Hour Division's WHISARD database, obtained via a Freedom of Information Act request. The database contains information on employers, violations, fines, and other details corresponding to __investigations__ concluded between October 1, 2001 and March 31, 2015. (Note: The WHD has redacted some tables and columns per FOIA exemption 5.) You can [download a copy of the database from the Internet Archive](https://archive.org/details/whd-enforcement-database-through-2015-03-31).

- The Office of Foreign Labor Certification's records of __visa-certification decisions__ for the H-2 visa program through December 2015. (The visa comes in two types: H-2A for agricultural workers and H-2B for unskilled non-agricultural workers.) Bulk, raw data is available [here](http://www.foreignlaborcert.doleta.gov/performancedata.cfm) and [here](http://www.flcdatacenter.com/). BuzzFeed News has [processed and standardized](https://github.com/BuzzFeedNews/H-2-certification-data) that data into a single file, which you can find [here](data/H-2-certification-decisions.csv). Newer certifications can be found on the [Department of Labor's iCert Portal](https://icert.doleta.gov/index.cfm?event=ehLCJRExternal.dspAdvJobOrderSearch).

- The Office of Foreign Labor Certification's lists of __debarred employers__. In November 2014, the OFLC provided BuzzFeed News with spreadsheets listing debarments issued between FY2009 and FY2013 for the H-2A program and between FY2009 and FY2014 for the H-2B program. BuzzFeed News identified additional debarments [via the Wayback Machine](https://web.archive.org/web/*/https://www.foreignlaborcert.doleta.gov/pdf/Debarment_List_Revisions.pdf) and by periodically scraping the [OFLC's public list of active debarments](https://www.foreignlaborcert.doleta.gov/pdf/Debarment_List_Revisions.pdf).

## Analyses

- __Passage__: "Between 2010 and 2014, agency investigators identified nearly 1,000 companies that had violated H-2 laws [...]"
- __Analysis__: The nearly-1,000-employer calculation can be found [here](notebooks/whd-investigations-and-violations.ipynb).

---

- __Passage__: "[...] yet in that time period, the Labor Department debarred fewer than 150."
- __Analysis__: You can find a list of OFLC debarments between 2010 and 2014 [here](data/debarments/debarments-2010-2014.csv). You can find a list of sources [here](data/debarments/sources.csv), and the sources themselves [here](data/debarments/source-documents/).

---

- __Passage__: "Twelve employers were found to have each stolen more than $100,000 from their guest workers in that time period; only one was debarred."
- __Analysis__: See [this previously-published list of the 12 employers](https://github.com/BuzzFeedNews/2015-07-h2-visas-and-enforcement/blob/master/data/manual-entry/top-total-h2-backwages-2010-2014-with-details.csv), and the [corresponding code](https://github.com/BuzzFeedNews/2015-07-h2-visas-and-enforcement/blob/master/notebooks/top-employer-back-wages.ipynb). Of the 12 employers, only Global Horizons Manpower was debarred.

---

- __Passage__: "Since forging that agreement, Popsy Pop has been approved for 140 visas [...]"
- __Analysis__: The agreement was [forged on Nov. 2, 2012](http://www.oalj.dol.gov/Decisions/ALJ/TNE/2012/WAGE_and_HOUR_DIVISI_v_POPSY_POP_LLC_2012TNE00007_\(NOV_02_2012\)_094321_CADEC_SD.PDF). You can find a table of Popsy Pop's certifications through December 2015 [here](data/certification-lists/popsy-pop-since-2012-11-02.csv). The company has been certified for an additional 34 workers in 2016, via two applications: [`H-400-15323-974876`](https://icert.doleta.gov/index.cfm?event=ehLCJRExternal.dspCert&doc_id=3&visa_class_id=7&id=84153) and [`H-400-15348-000984`](https://icert.doleta.gov/index.cfm?event=ehLCJRExternal.dspCert&doc_id=3&visa_class_id=7&id=87838).


---

- __Passage__: "One of those companies has gained certification for more than 5,400 visas since its founding in August 2014."
- __Analysis__: The company is National Agricultural Consultants. (For more background, see [this BuzzFeed News investigation](https://www.buzzfeed.com/kenbensinger/the-coyote) from December 2015.) You can find a table of NAC's certifications through December 2015 [here](data/certification-lists/national-agricultural-consultants-since-2014-08-03.csv).

---

- __Passage__: "Meanwhile, agency investigators found 68 violations of worker protection laws over the course of four different investigations of Altendorf Transport, and calculated that it owed employees over $22,000 in back wages."
- __Analysis__: You can find a list of the investigations and violation counts [here](notebooks/whd-investigations-and-violations.ipynb).

---

- __Passage__: "T. Bell Detasseling [...] with more than 6,800 visas approved between 2005 and 2015 [...]"
- __Analysis__: You can find a table of all T. Bell certifications from FY 2006 (which began in Oct. 2005) through calendar year 2015 [here](data/certification-lists/t-bell-fy-2006-through-cy-2015.csv).

---

- __Passage__: "Three previous probes of the company had turned up a whopping 1,466 violations of worker protection laws, ranging from wage theft to poor record keeping to failure to ensure that workers left the country when their jobs were done."
- __Analysis__: You can find a list of the investigations and violation counts [here](notebooks/whd-investigations-and-violations.ipynb).

---

- __Passage__: "T. Bell [...] has received approval for at least 473 visas since Jan. 30, 2015, the date investigators submitted their final report [...]"
- __Analysis__: You can find a table of all T. Bell certifications since that date through December 2015 [here](data/certification-lists/t-bell-since-2015-01-30.csv).

---

- __Passage__: "[Vasquez Citrus], which has been approved for more than 1,000 visas since 2013"
- __Analysis__: You can find a table of certifications for Vasquez Citrus (directly, or via Juan or Roberto Vasquez) through December 2015 [here](data/certification-lists/vasquez-citrus.csv). The company has been certified for an additional 390 workers in 2016, via three applications: [`H-300-15338-273530`](https://icert.doleta.gov/index.cfm?event=ehLCJRExternal.dspCert&doc_id=3&visa_class_id=8&id=84771), [`H-300-16004-246335`](https://icert.doleta.gov/index.cfm?event=ehLCJRExternal.dspCert&doc_id=3&visa_class_id=8&id=86603), and [`H-300-16081-864237`](https://icert.doleta.gov/index.cfm?event=ehLCJRExternal.dspCert&doc_id=3&visa_class_id=8&id=93175).

---

## Feedback

If you have questions or feedback about the data or analyses, contact Jeremy Singer-Vine at jeremy.singer-vine@buzzfeed.com.

Looking for more from BuzzFeed News? [Click here for a list of our open-sourced projects, data, and code](https://github.com/BuzzFeedNews/everything).
