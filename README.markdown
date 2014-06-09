## What is Octopress?

Octopress is [Jekyll](https://github.com/mojombo/jekyll) blogging at its finest.

1. **Octopress sports a clean responsive theme** written in semantic HTML5, focused on readability and friendliness toward mobile devices.
2. **Code blogging is easy and beautiful.** Embed code (with [Solarized](http://ethanschoonover.com/solarized) styling) in your posts from gists, jsFiddle or from your filesystem.
3. **Third party integration is simple** with built-in support for Pinboard, Delicious, GitHub Repositories, Disqus Comments and Google Analytics.
4. **It's easy to use.** A collection of rake tasks simplifies development and makes deploying a cinch.
5. **Ships with great plug-ins** some original and others from the Jekyll community &mdash; tested and improved.


## Documentation

Check out [Octopress.org](http://octopress.org/docs) for guides and documentation.


## Contributing

[![Build Status](https://travis-ci.org/imathis/octopress.png?branch=master)](https://travis-ci.org/imathis/octopress)

We love to see people contributing to Octopress, whether it's a bug report, feature suggestion or a pull request. At the moment, we try to keep the core slick and lean, focusing on basic blogging needs, so some of your suggestions might not find their way into Octopress. For those ideas, we started a [list of 3rd party plug-ins](https://github.com/imathis/octopress/wiki/3rd-party-plugins), where you can link your own Octopress plug-in repositories. For the future, we're thinking about ways to easier add them them into our main releases.


## License
(The MIT License)

Copyright © 2009-2013 Brandon Mathis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ‘Software’), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ‘AS IS’, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#### If you want to be awesome.
- Proudly display the 'Powered by Octopress' credit in the footer.
- Add your site to the Wiki so we can watch the community grow.


##  Modify (by Chenxiaohui)

### pandoc support

create a markdown file in source/pandoc, use {% pandoc test.md %} to include this file in. Blog will generate html from this markdown and include the html.

use snippets tab to create table, pan to insert pandoc syntax

### indent support

lines start with two spaces will generate a two-word indent. eg:

    no indent

      indent

      * item (space will be ignored)

    > * indent item
      * indent item 2

effect

    ![effect](effect.png "effect")

### image support

there are three kind of image syntax:

     {% img  /images/2014-5 "title text" "title text" %}
     {% img img-polaroid center /images/2013-10 "title text" "title text" %}
     ![alt](url "title")

img src directory is source/images/

rsz.sh helps you  resize file

use img/im snippets to create table

### refs

ref has three types:

    [1]: url   "alt"
    [2]:
    [3]:

    [id]: mailto:url   "alt"
    [id]

    [id]: url   "alt"
    [id]

sublime snippets helps to make refs. and generateref plugin helps to make refs list.


### more

<!--more--> separates page


### isolate, integrate

isolate moves other docs into stash, integrate moves stashs to posts


### hiearchy

    # first
    ## sec
    ## third
    ** bold **
    no indent
    * item
      indent
      > * indent item

### octopress sublime plugin

isolate/generate/preview is useful

### exceptions

if needs to write code in item list, use double indent. eg:

* item
        code
        {
        }
* item
