# README
These are the files for the book [Learn to Code with Baseball](https://codebaseball.com).

If you're not familiar with Git or GitHub, no problem. Just click the `Source
code` link under the latest release to download the files.  This will download
a file called `ltcwbb-files-vX.X.X.zip`, where X.X.X is the latest version.

When you unzip these (note in the book I've dropped the version number and
renamed the directory just `ltcwbb-files`, which you can do too) you'll see
four sub-directories: `code`, `data`, `anki`, `solutions-to-excercises`.

You don't have to do anything with these right now except know where you put
them. For example, on my mac, I have them in my home directory:

`/Users/nathanbraun/ltcwbb-files`

If I were using Windows, it might look like this:

`C:\Users\nathanbraun\ltcwbb-files`

Set these aside for now and we'll pick them up in chapter 2.

## Changelog
### v0.9.7 (2024-02-07)
Minor typos.

### v0.9.5 (2023-09-21)
Minor typos (thanks Paul!).

### v0.9.4 (2023-09-21)
Minor typos (thanks John!).

### v0.9.2 (2023-03-14)
Fixed some typos (thanks Matthew!).

### v0.9.1 (2023-01-01)
Fixed some formatting and footnote typos (thanks Paul!).

### v0.9.0 (2022-12-13)
Rewrote and expanded API chapter since old API stopped working (see issue
[#3][i3] - thanks @lozdog245 for brining to my attention). Also added section on using the excellent [MLB-StatsAPI](
[https://github.com/toddrob99/MLB-StatsAPI](https://github.com/toddrob99/MLB-StatsAPI)) package. 

### v0.8.2 (2022-07-28)
Minor rewording.

### v0.8.1 (2022-07-28)
Updated Anki cards, tweaked some Python language and fixed a typo (thanks
Aaron!)

### v0.7.1 (2022-02-28)
Added a note explaining *granularity* in the main text, before asking any end of
chapter exercises on it (see issue [#2][i2])

### v0.7.0 (2022-02-28)
Pretty big update to scraping section to make things clearer.

Also added note on 403 response issue people were running into while scraping
Baseball Almanac. Thanks to everyone who emailed me about this.

### v0.6.1 (2021-12-24)
Updated file path in random forest section (see issue [#1][i1])

### v0.6.0 (2021-11-18)
Add end of chapter exercises for scraping and visualization (more coming soon).
Thanks Chris!

### v0.5.0 (2021-06-22)
Expanded visualization section to include scatter and line plots.

### v0.4.2 (2021-06-17)
Fixed some scraping in book to match what was in the code (thanks Greg, Nick!)

Fixed typo in exercise 3.3.2 and made changed LAA -> ANA in teams.csv (thanks
Lennart and Tim!)

Fixed a few typos + stray football references (thanks Brooks, Mark!)

### v0.4.1 (2021-06-16)
Updated visualization section + associated homework problems to use Seaborn
0.11.x (September 2020), which added a new `displot` function. This means
making our distribution plots change from, say:

```python
g = (sns.FacetGrid(df)
     .map(sns.kdeplot, 'mpg', shade=True))
```

To:

```python
g = sns.displot(df, x='mph', kind='kde', fill=True)
```

It also opens up some new possibilities (e.g. with plotting empirical CDFs)
that I might discuss in a future update.

### v0.3.0
Add this changelog, bundle files in an github release vs including with SendOwl.

[i1]: https://github.com/nathanbraun/ltcwbb-files/issues/1
[i2]: https://github.com/nathanbraun/ltcwbb-files/issues/2
[i3]: https://github.com/nathanbraun/ltcwbb-files/issues/3
