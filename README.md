# maubot-dmutil
A simple matrix plugin for [maubot](https://github.com/maubot/maubot), which tracks direct message rooms

## Installation
Simply drag the plugin into the plugin folder, or upload it via maubot's user interface. You can download the plugin from the [releases](/releaes).

## What it does
This plugin stores whether a room the bot joins is a direct message room. For this the bot sets the `account_data` event of the Matrix API.
Also, the bot automatically leaves rooms where there are no participants.
