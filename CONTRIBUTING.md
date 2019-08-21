# Contributing to T_System

:sparkles: First off all, thanks for taking the time to contribute! :sparkles:

The following is a set of guidelines for contributing to T_System an open source (non-)moving objects tracking system via two axis camera motion (and as optionally n joint robotic arm) project, which is hosted in the [connected-life Organization](https://github.com/connected-life) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

- [Code of Conduct](#code-of-conduct)

- [Getting Started](#getting-started)
  - [Fork The Repo](#fork-the-repo)
    - [Step 1: Set Up Git](#step-1-set-up-git)
    - [Step 2: Fork The Repo](#step-2-fork-the-repo)
    - [Step 3: Create a local clone of your fork](#step-3-create-a-local-clone-of-your-fork)
  - [Install T_System in Development Mode](#install-t_system-in-development-mode)
    - [Use It](#use-it)
    - [Choice for Code Editor](#choice-for-code-editor)
    - [About Packaging](#about-packaging)

- [How Can I Contribute?](#how-can-i-contribute)
  - [Decide What To Do](#decide-what-to-do)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Projects](#projects)
    - [Your First Code Contribution](#your-first-code-contribution)
  - [Push & Pull](#push--pull)
    - [Step 1: Go to the local clone of your fork](#step-1-go-to-the-local-clone-of-your-fork)
    - [Step 2: Pull the Latest Changes](#step-2-pull-the-latest-changes)
    - [Step 3: Write Your Code](#step-3-write-your-code)
    - [Step 4: Push To Your Fork](#step-4-push-to-your-fork)
    - [Step 5: Creating a Pull Request](#step-5-creating-a-pull-request)

- [Styleguides](#styleguides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)

- [Troubleshooting](https://github.com/connected-life/T_System/blob/master/docs/TROUBLESHOOTING.md#troubleshooting)


## Code of Conduct

This project and everyone participating in it is governed by the [T_System's Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [cem.baybars@gmail.com](mailto:cem.baybars@gmail.com).

#### I don't want to read this whole thing I just have a question!!!

> **Note:** Please don't file an issue to ask a question. You'll get faster results by using the resources below.

We have an official [chat room on Gitter](https://gitter.im/connected-life/community) where the community chimes in with helpful advice if you have questions.


## Getting Started

|                         |                                         |
|-------------------------|-----------------------------------------|
| **Operating systems**   | Linux                                   |
| **Python versions**     | Python 3.x (64-bit)                     |
| **Distros**             | Raspbian                                |
| **Package managers**    | APT, pip                                |
| **Languages**           | English                                 |
|                         |                                         |

**Supported Distributions:** Raspbian. This release is fully supported. Any other Debian based ARM architecture distributions are partially supported.

### Fork The Repo

#### Step 1: Set Up Git

If you haven't yet, you should first [set up Git](https://help.github.com/articles/set-up-git). Don't forget to [set up authentication to GitHub from Git](https://help.github.com/articles/set-up-git#next-steps-authenticating-with-github-from-git) as well.

#### Step 2: Fork The Repo

Forking a repository is a simple two-step process:

<img src="http://i.imgur.com/XlXtYBV.png" width="300" align="right" />

1. On GitHub, navigate to the [connected-life/T_System](https://github.com/connected-life/T_System) repository.
2. In the top-right corner of the page, click **Fork**.

That's it! Now, you have a **fork** of the original T_System repository under your account.

#### Step 3: Create a local clone of your fork

Right now, you have a fork of the T_System repository, but you don't have the files in that repository on your computer. Let's create a *clone* of your fork locally on your computer:

<img src="http://i.imgur.com/jB2aFXQ.png" width="300" align="right" />

1. On GitHub, navigate to **your fork** of the T_System repository.
2. Under the repository name, click **Clone or download**.
3. Copy the given clone URL in the **Clone with HTTPs** section.
4. Open Terminal
5. Type `git clone`, and then paste the URL you copied in Step 2. It will look like this, with your GitHub username instead of `YOUR-USERNAME`:

```
git clone https://github.com/YOUR-USERNAME/T_System.git
```

6. Press **Enter**. Your local clone will be created:

```Shell
git clone https://github.com/YOUR-USERNAME/T_System.git
Cloning into 'T_System'...
remote: Enumerating objects: 1863, done.
remote: Total 1863 (delta 0), reused 0 (delta 0), pack-reused 1863
Receiving objects: 100% (1863/1863), 21.48 MiB | 2.04 MiB/s, done.
Resolving deltas: 100% (1253/1253), done.
Checking connectivity... done.
```

### Install T_System in Development Mode

You need to install T_System with `sudo` rights, even if you are installing editable/development mode.

```Shell
git clone https://github.com/YOUR-USERNAME/T_System.git
cd T_System/
chmod +x install-dev.sh
sudo ./install-dev.sh
```

#### Use It

Try to experience every command listed in [README.md](https://github.com/DragonComputer/T_System#Usage). Please watch [this playlist]() if you did not understand how to use T_System.

If you face with a problem while installing or using T_System then please take a look at the [Troubleshooting](https://github.com/connected-life/T_System/blob/master/docs/TROUBLESHOOTING.md#troubleshooting) section for the cases that fitting to your situation. Our [chat room on Gitter](https://gitter.im/connected-life/community) is also a viable option for support requests.

#### Choice for Code Editor

We use [PyCharm editor](https://www.jetbrains.com/pycharm/) with tabs(four whitespaces) without auto-indentation. Indentation mistakes can be troublesome in Python, please don't send files with messed up indentations.

#### About Packaging

If you are wondering about the package structure and distribution then please take a look to the official [Packaging and Distributing Projects](https://packaging.python.org/tutorials/distributing-packages/) tutorial of Python.


## How Can I Contribute?

### Decide What To Do

#### Reporting Bugs

If you think you found a bug in T_System then first please check the all cases listed in [Troubleshooting](https://github.com/connected-life/T_System/blob/master/docs/TROUBLESHOOTING.md#troubleshooting) section. If you still think that's a bug then please [file an issue](https://github.com/connected-life/T_System/issues/new) immediately. Don't forget to mention that it's a bug or something going on very wrong.

<!-- This section guides you through submitting a bug report for T_System. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:. -->

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Suggesting Enhancements

If you have an enhancement idea or you are not happy with an ugly piece of code then please [file an issue](https://github.com/connected-life/T_System/issues/new) and mention that it's an enhancement proposal.

<!-- This section guides you through submitting an enhancement suggestion for T-System, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:. -->

#### Projects

Look at the cards pinned to **To Do** columns inside [open projects](https://github.com/connected-life/T_System/projects) to find something suitable for you. If you are willing to take a card/task from there then contact with project maintainers via [Gitter chat room](https://gitter.im/connected-life/community) so they will assign that task to you.

#### Your First Code Contribution

Unsure where to begin contributing to T_System? You can start by looking through these `beginner` and `help-wanted` issues:

 - [Beginner issues][beginner] which should only require a few lines of code, and a test or two.
 - [Help wanted issues][help-wanted] which should be a bit more involved than `beginner` issues.
 - [Missing dependency issues][missing-dependency] which should be mostly platform/distro related issues.
 - [Enhancement proposals][enhancement] which should be improvements ideas or alteration proposals on code.
 - [Bugs][bug] which should be issued with proof of existence and expected to be hard to fix.

Now you must have decided what to do. Before starting to write some code, take a quick look to [PEP 8](https://www.python.org/dev/peps/pep-0008/) - [because](#python-styleguide) :point_down:

### Push & Pull

For working well disciplined, you need to know how to deal with **git**'s push and pull mechanisms.

#### Step 1: Go to the local clone of your fork

Now `cd` into the local clone of your fork. Wherever the folder of T_System is:

```
cd T_System/
```

#### Step 2: Pull the Latest Changes

Now make sure your repository is up to date first using:

```
git pull origin master
```

#### Step 3: Write Your Code

At this step you are free to make any changes inside the local clone of your fork. Make sure that your changes serve to **single well defined goal** which will be your commit message. **DO NOT** try to achieve multiple (and unrelated) tasks with a single commit.

Before proceeding to Step 4, make sure that you have done all the tests and you did not break any existing feature of T_System.

#### Step 4: Push To Your Fork

When you are done, you must push your changes from the local clone to your fork with:

```
git add -A
git commit -m "Change this functionality from here to there"
git push -u origin master
```

<sup>Replace the message in `git commit -m "Change this functionality from here to there"` line with your actual message.</sup>

#### Step 5: Creating a Pull Request

Now follow [this tutorial](https://help.github.com/articles/creating-a-pull-request/) to create a pull request. You will create your pull request via [this page](https://github.com/connected-life/T_System/compare).

Once you have successfully created the pull request, wait for a response from the project maintainers. If your patch is OK then we will merge it within approximately 24 hours.

## Style Guides

### Available Grammar

  - `@TODO`: Something to be done
  - [`@FIXME`](#bug-report): Bug Report, should be corrected, Marked with :bug: Commit
  - `@CHANGED`: Version Changes together with `@SINCE` DocComment, _Usually_ Marked with :fire: or :zap: Commits
  - `@XXX`: Warn other programmers of problematic or misguiding code
  - `@IDEA`: A New Idea or Proof-of-Concept, Marked with :bulb: Commit
  - `@HACK`: Workaround or Customer Customizations, Marked with :ribbon: Commit
  - `@NOTE`: Add attention to something Important
  - `@REVIEW`: Needs to be Audited/Reviewed Immediately, _Usually_ Marked with :construction: Commit

### Bug Report
----------
1. Add `@FIXME` Comment above SourceCode where Bug/Exception was Occurred.
2. Write Additional Information:
    1. Steps to Reproduce the Error
    2. `Exception` Message and Code
    3. Expected Result
    4. Actual Result
    5. Environment Detail
3. Mention the Task ID in Format `{T###}`.
4. (optional) Add Screenshots in Format `{F###}`(_Phabricator Specific_).
5. Commit the Comments(with :bug: Emoji), also include Items 2.B, 3 & 4 in Commit Message too.
6. Award that Task with `Manufacturing Defect` Token(_Phabricator Specific_).

### Notes
-----
- Do **NOT** edit Contents of `Vendor` files(Composer, Bower, ...).
- Grammars Should Appear in a List/Window in Your IDE of Choice([PHPStorm](https://www.jetbrains.com/help/phpstorm/2016.2/defining-todo-patterns-and-filters.html)).
- There Must be an Audit for this Bug(Commit) Appear in Phabricator.
- These Kind of Bug Reports Remain in History of VCS for future References of that Scope of Code.
- All Attached Files & Commit Reference HashTag will be Referenced in the Phabricator Task View.
- These Audits May become Tasks Later.

### Git Commit Messages

 - Use the present tense ("Add feature" not "Added feature")
 - Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
 - Limit the first line to 72 characters or less
 - Reference issues and pull requests liberally after the first line

#### Consider starting the commit message with an applicable emoji:

| Emoji | Raw Emoji Code | Description |
|:---:|:---:|---|
| :art: | `:art:` | when improving the **format**/structure of the code |
| :newspaper: | `:newspaper:` | when creating a **new file** |
| :pencil: | `:pencil:` | when **performing minor changes/fixing** the code or language |
| :racehorse: | `:racehorse:` | when improving **performance** |
| :books: | `:books:` | when writing **docs** |
| :bug: | `:bug:` | when reporting a **bug**, with [`@FIXME`](https://github.com/slashsbin/styleguide-todo-grammar#bug-report)Comment Tag |
| :ambulance: | `:ambulance:` | when fixing a **bug** |
| :penguin: | `:penguin:` | when fixing something on **Linux** |
| :apple: | `:apple:` | when fixing something on **Mac OS** |
| :checkered_flag: | `:checkered_flag:` | when fixing something on **Windows** |
| :fire: | `:fire:` | when **removing code** or files, _maybe_ with `@CHANGED` Comment Tag |
| :tractor: | `:tractor:` | when **change file structure**. Usually together with :art: |
| :hammer: | `:hammer:` | when **refactoring** code |
| :umbrella: | `:umbrella:` | when adding **tests** |
| :microscope: | `:microscope:` | when adding **code coverage** |
| :green_heart: | `:green_heart:` | when fixing the **CI** build |
| :lock: | `:lock:` | when dealing with **security** |
| :arrow_up: | `:arrow_up:` | when upgrading **dependencies** |
| :arrow_down: | `:arrow_down:` | when downgrading **dependencies** |
| :fast_forward: | `:fast_forward:` | when **forward-porting features** from an older version/branch |
| :rewind: | `:rewind:` | when **backporting features** from a newer version/branch |
| :shirt: | `:shirt:` | when removing **linter**/strict/deprecation warnings |
| :lipstick: | `:lipstick:` | when improving **UI**/Cosmetic |
| :wheelchair: | `:wheelchair:` | when improving **accessibility** |
| :globe_with_meridians: | `:globe_with_meridians:` | when dealing with **globalization**/internationalization/i18n/g11n |
| :construction: | `:construction:` | **WIP**(Work In Progress) Commits, _maybe_ with `@REVIEW` Comment Tag |
| :gem: | `:gem:` | New **Release** |
| :egg: | `:egg:` | New **Release** with Python egg|
| :ferris_wheel: | `:ferris_wheel:` | New **Release** with Python wheel package |
| :bookmark: | `:bookmark:` | Version **Tags** |
| :tada: | `:tada:` | **Initial** Commit |
| :speaker: | `:speaker:` | when Adding **Logging** |
| :mute: | `:mute:` | when Reducing **Logging** |
| :sparkles: | `:sparkles:` | when introducing **New** Features |
| :zap: | `:zap:` | when introducing **Backward-InCompatible** Features, _maybe_ with `@CHANGED` Comment Tag |
| :bulb: | `:bulb:` | New **Idea**, with `@IDEA` Comment Tag |
| :snowflake: | `:snowflake:` | changing **Configuration**, Usually together with :penguin: or :ribbon: or :rocket: |
| :ribbon: | `:ribbon:` | Customer requested application **Customization**, with `@HACK` Comment Tag |
| :rocket: | `:rocket:` | Anything related to Deployments/**DevOps** |
| :elephant: | `:elephant:` | **PostgreSQL** Database specific (Migrations, Scripts, Extensions, ...)  |
| :dolphin: | `:dolphin:` | **MySQL** Database specific (Migrations, Scripts, Extensions, ...) |
| :leaves: | `:leaves:` | **MongoDB** Database specific (Migrations, Scripts, Extensions, ...) |
| :bank: | `:bank:` | **Generic Database** specific (Migrations, Scripts, Extensions, ...) |
| :whale: | `:whale:` | **Docker** Configuration |
| :handshake: | `:handshake:` | when **Merge files** |
| :cherries: | `:cherries:` | when Commit Arise from one or more [**Cherry-Pick**](https://git-scm.com/docs/git-cherry-pick) Commit(s) |

### Python Style Guide

All Python must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).

[beginner]:https://github.com/connected-life/T_System/issues?q=is%3Aissue+is%3Aopen+label%3Abeginner
[help-wanted]:https://github.com/connected-life/T_System/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
[missing-dependency]:https://github.com/connected-life/T_System/issues?q=is%3Aissue+is%3Aopen+label%3A%22missing+dependency%22
[enhancement]:https://github.com/connected-life/T_System/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement
[bug]:https://github.com/connected-life/T_System/issues?q=is%3Aissue+is%3Aopen+label%3Abug

##### References
  - <sup>https://en.wikipedia.org/wiki/Comment_(computer_programming)#Tags</sup>
  - <sup>https://softwareengineering.stackexchange.com/questions/65467/what-does-xxx-mean-in-a-comment</sup>
  - <sup>https://github.com/DragonComputer/Dragonfire/blob/master/CONTRIBUTING.md</sup>
  - <sup>https://github.com/slashsbin/styleguide-git-commit-message/blob/master/README.md</sup>
