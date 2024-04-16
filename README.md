# Memos - Alfred Workflow

This Alfred workflow allows you to search and send [memos](https://github.com/usememos/memos) using access token (requires version > 0.15)

## Prerequisites

This workflow requires Alfred version > 5.5 to enable Text View

## Setup

You need to set two environmental variables:

- `host`: The base URL for your memos instance.
- `token`: Memos access token for authentication.

## Features

### 1 List and search Memos

You can search for memos containing specific words or phrases via the list memo keyword. Comments and memos are displayed with different icon and subtitle, you can filter them by adding `memo` or `comment` in your query.

On selected item:

- **Enter**: Open selected memo in your browser.
- **Cmd + Enter ** Opens a detailed text view of the memo.
- **Option + Enter** Copies the memo content to the clipboard.

### 2 Send Memos

You can send memos by entering content directly into Alfred, which will post the memo to your backend using an API. You can specify visibility (e.g., public, private) using different keywords.

## Thanks

- Comment icon created by [Smashicons - Flaticon](https://www.flaticon.com/free-icons/comment)
- Memos icon from https://www.usememos.com/
