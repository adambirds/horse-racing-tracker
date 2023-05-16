# Horse Racing Tracker

## Description

This is a simple script that tracks when a horse or list of horses are running in either the UK or Ireland and provides a notification when they are running.
The app uses the [Sporting Life](https://www.sportinglife.com/) website to get the information about the horses.

The notifications will contain information such as:

* Meeting, Date and Race Time
* Jockey and Trainer
* Horse Age and Sex
* Form
* Odds
* Commentary (if available)
* Last Ran (if available)

We currently support the following notification methods:

* Discord Webhook

## Configuration

To configure the script, you will need to edit the `config.yaml` file.

You simply need to ass your horses to the `horses_to_watch` key and add your Discord Webhook URL to the `DISCORD_WEBHOOK_URL` key.

## Features Coming Soon

* Email Notifications
* Text/WhatsApp Notifications (Possibly)

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE v3](https://github.com/adambirds/horse-racing-tracker/blob/main/LICENSE).