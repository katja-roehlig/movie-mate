# MovieMate 🎬

A web-based movie library application built with **Python** and **Flask**. This project allows users to create simple profiles, manage their personal movie collections, and automatically fetch movie details using an external API.

## 🚀 Features

- **User Profiles:** Simple name-based profile creation (no password required).
- **Public Landing Page:** Overview of all existing user profiles.
- **Dynamic Movie Search:** Add movies by title. The app automatically fetches data (Year, Director, Poster) from the **OMDb API**.
- **Personal Collections:** Each user has a unique collection where movies are linked via a Foreign Key.
- **Full CRUD Functionality:**
  - **Create:** Add new movies to your list.
  - **Read:** View your collection with high-quality posters and info.
  - **Update:** Rate your movies (default starts at 0.0).
  - **Delete:** Remove movies from your collection.

## 🛠️ Tech Stack

- **Backend:** Python / Flask
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Frontend:** HTML5, CSS3, Jinja2 Templates
- **API Integration:** OMDb (Open Movie Database)

## 📊 Database Schema

The application uses two main tables with a **One-to-Many** relationship:

1.  **User Table:** Stores `id` (Primary Key) and `username`.
2.  **Movie Table:** Stores `id`, `title`, `year`, `director`, `image_url`, `rating`, and `user_id` (Foreign Key).
    *   *Note:* If two users add the same movie, it is stored as two separate entries to allow individual ratings and management.

## 🎨 UI/UX Highlights

- **Streaming-Service Look:** Modern dark mode design inspired by popular streaming platforms.
- **Interactive Modals:** Uses native HTML `<dialog>` elements for delete confirmations and rating updates.

