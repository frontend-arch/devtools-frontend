# Chrome DevTools frontend

<!-- [START badges] -->
[![NPM package](https://img.shields.io/npm/v/chrome-devtools-frontend.svg)](https://npmjs.org/package/chrome-devtools-frontend)
<!-- [END badges] -->

The client-side of the Chrome DevTools, including all JS & CSS to run the DevTools webapp.

### Source code
The frontend is available on [chromium.googlesource.com](https://chromium.googlesource.com/devtools/devtools-frontend).

### Workflows

In order to make changes to DevTools frontend, build, run, test, and submit changes, several workflows exist. Having [depot_tools](https://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/depot_tools_tutorial.html#_setting_up) set up is a common prerequisite.

#### Standalone workflow
As a standalone project, Chrome DevTools frontend can be checked out and built independently from Chromium. The main advantage is not having to check out and build Chromium. However, there is also no way to run layout tests in this workflow.
<details>

##### Checking out source

To check out the source for DevTools frontend only, follow these steps:

```bash
mkdir devtools
cd devtools
git clone https://chromium.googlesource.com/devtools/devtools-frontend
gclient config https://chromium.googlesource.com/devtools/devtools-frontend --unmanaged
```

##### Build

To build, follow these steps:
```bash
cd devtools-frontend
gclient sync
gn gen out/Default
autoninja -C out/Default
```
The resulting build artifacts can be found in `out/Default/resources/inspector`.

##### Run in Chromium

These steps work with Chromium 79 or later.
To run the production build, use

**(Requires `brew install coreutils` on Mac.)**

```bash
<path-to-chrome>/chrome --custom-devtools-frontend=file://$(realpath out/Default/resources/inspector)
```

To run the debug build (directly symlinked to the original unminified source files),
build both Chromium and DevTools frontend with the [GN flag](https://www.chromium.org/developers/gn-build-configuration) `debug_devtools=true`, and use

```bash
<path-to-chrome>/chrome --custom-devtools-frontend=file://$(realpath out/Default/resources/inspector/debug)
```

You can inspect DevTools with DevTools by undocking DevTools and then open the developers tools (F12 on Windows/Linux, Cmd+Option+I on Mac).

##### Test
Test are available by running scripts in `scripts/test/`.

##### Create a change
Usual [steps](https://chromium.googlesource.com/chromium/src/+/master/docs/contributing.md#creating-a-change) for creating a change work out of the box.

##### Managing dependencies
- To sync dependencies from Chromium to DevTools frontend, use `scripts/deps/roll_deps.py`.
- To roll the HEAD commit of DevTools frontend into Chromium, use `scripts/deps/roll_to_chromium.py`.
- To update DevTools frontend's DEPS, use `roll-dep`.
</details>

#### Chromium workflow
DevTools frontend can also be developed as part of the full Chromium checkout.
<details>

##### Checking out source
Follow [instructions](https://www.chromium.org/developers/how-tos/get-the-code) to check out Chromium. DevTools frontend can be found under `third_party/devtools-frontend/src/`.

##### Build
Refer to [instructions](https://www.chromium.org/developers/how-tos/get-the-code) to build Chromium. To only build DevTools frontend, use `devtools_frontend_resources` as build target. The resulting build artifacts for DevTools frontend can be found in `out/Default/resources/inspector`.

Consider building with the [GN flag](https://www.chromium.org/developers/gn-build-configuration) `debug_devtools=true` to symlink to the original unminified source.

##### Run
Run Chrome with DevTools frontend bundled:
```bash
out/Default/chrome
```

##### Test
Test are available by running scripts in `third_party/devtools-frontend/src/scripts/test/`.
After building content shell, we can also run layout tests that are relevant for DevTools frontend:
```bash
autoninja -C out/Default content_shell
third_party/blink/tools/run_web_tests.py http/tests/devtools
```

##### Create a change
Usual [steps](https://chromium.googlesource.com/chromium/src/+/master/docs/contributing.md#creating-a-change) for creating a change work out of the box, when executed in `third_party/devtools-frontend/src/`.
</details>

#### Integrate standalone checkout into Chromium
If you prefer working on a standalone checkout of DevTools frontend, but want to build, test, and run inside the full Chromium checkout. This way, you combine the best of both worlds.
<details>

Disable `gclient sync` for DevTools frontend inside of Chromium by editing `.gclient` config. From `chromium/src/`, simply run
```bash
vim $(gclient root)/.gclient
```

In the `custom_deps` section, insert this line:
```python
"src/third_party/devtools-frontend/src": None,
```

Then run
```bash
gclient sync -D
```
This removes the DevTools frontend dependency. We now create a symlink to refer to the standalone checkout:

**(Note that the folder names do NOT include the trailing slash)**

```bash
ln -s path/to/standalone/devtools-frontend third_party/devtools-frontend/src
```

</details>

Running `gclient sync` in `chromium/src/` will update dependencies for the Chromium checkout. Running `gclient sync` in `chromium/src/third_party/devtools-frontend/src` will update dependencies for the standalone checkout.

### Testing
Please refer to the [overview document](https://docs.google.com/document/d/1c2KLKoFMqLB2A9sNAHIhYb70XFyfBUBs5BZSYfQAT-Y/edit). The current test status can be seen at the [test waterfall].

### Additional references
* DevTools documentation: [devtools.chrome.com](https://devtools.chrome.com)
* [Debugging protocol docs](https://developer.chrome.com/devtools/docs/debugger-protocol) and [Chrome Debugging Protocol Viewer](http://chromedevtools.github.io/debugger-protocol-viewer/)
* [awesome-chrome-devtools](https://github.com/paulirish/awesome-chrome-devtools): recommended tools and resources
* Contributing to DevTools: [bit.ly/devtools-contribution-guide](http://bit.ly/devtools-contribution-guide)
* Contributing To Chrome DevTools Protocol: [docs.google.com](https://docs.google.com/document/d/1c-COD2kaK__5iMM5SEx-PzNA7HFmgttcYfOHHX0HaOM/edit?usp=sharing)

### Useful Commands

#### `npm run format-py`
Formats your Python code using [yapf](https://github.com/google/yapf)

> Note: Yapf is a command line tool. You will have to install this manually, either from PyPi through `pip install yapf` or if you want to enable multiprocessing in Python 2.7, `pip install futures`

### Source mirrors
DevTools frontend repository is mirrored on [GitHub](https://github.com/ChromeDevTools/devtools-frontend).

DevTools frontend is also available on NPM as the [chrome-devtools-frontend](https://www.npmjs.com/package/chrome-devtools-frontend) package. It's not currently available via CJS or ES2015 modules, so consuming this package in other tools may require [some effort](https://github.com/paulirish/devtools-timeline-model/blob/master/index.js).

The version number of the npm package (e.g. `1.0.373466`) refers to the Chromium commit position of latest frontend git commit. It's incremented with every Chromium commit, however the package is updated roughly daily.

### Getting in touch
* All devtools commits: [View the log] or follow [@DevToolsCommits] on Twitter
* [All open DevTools tickets] on crbug.com
* File a new DevTools ticket: [new.crbug.com](https://bugs.chromium.org/p/chromium/issues/entry?labels=OS-All,Type-Bug,Pri-2&components=Platform%3EDevTools)
* Code reviews mailing list: [devtools-reviews@chromium.org]
* [@ChromeDevTools] on Twitter
* Chrome DevTools mailing list: [groups.google.com/forum/google-chrome-developer-tools](https://groups.google.com/forum/#!forum/google-chrome-developer-tools)

  [devtools-reviews@chromium.org]: https://groups.google.com/a/chromium.org/forum/#!forum/devtools-reviews
  [View the log]: https://chromium.googlesource.com/devtools/devtools-frontend/+log/master
  [@ChromeDevTools]: http://twitter.com/ChromeDevTools
  [@DevToolsCommits]: http://twitter.com/DevToolsCommits
  [all open DevTools tickets]: https://bugs.chromium.org/p/chromium/issues/list?can=2&q=component%3APlatform%3EDevTools&sort=&groupby=&colspec=ID+Stars+Owner+Summary+Modified+Opened
  [test waterfall]: https://ci.chromium.org/p/devtools-frontend/g/main/console
