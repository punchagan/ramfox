# Ramfox

A Firefox extension that sort of makes it behave like Rambox

## Why?

I like Rambox for some of the features it has (see planned features section
below), but it feels like the wheel is being re-invented, in [some
cases](https://github.com/saenzramiro/rambox/issues/509).

I'd like to use a standard browser, with some additional functionality.

## Planned features

- [ ] DND mode

    - [ ] Turn notifications on/off
    - [ ] Show/Hide unread counts

- [ ] Master password on Launch

- [ ] Master password at run-time (optional)

- [X] Open all links in the default browser

## Setup ##

This add-on is a native extension with a lot of hacks that "work for me". It may
never be published to the Mozilla Addons Directory.

1. Clone this repository
2. Install [web-ext](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Getting_started_with_web-ext#Installation)
3. Create a new profile in Firefox
4. Run the script `run.py` passing the path of the profile you created as the
   `--profile-dir` argument

   ```sh
   $ /run.py --profile-dir ~/.mozilla/firefox-trunk/plpouotz.Chat/ --firefox-binary firefox-trunk
   ```

**NOTE**: Windows is not yet supported

## License

This extension is a fork of the [native messaging
example](https://github.com/mdn/webextensions-examples/tree/master/native-messaging)
and is licensed under the Mozilla Public License 2.0.
