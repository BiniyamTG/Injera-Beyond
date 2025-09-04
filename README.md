# Injera & Beyond API

A FastAPI and MongoDB-based RESTful API for exploring Ethiopian cuisine, designed for tourists. It provides full CRUD operations for foods and drinks, with features like random suggestions, regional filtering, user favorites, and cultural trivia.

## Features
- **Food & Drink Details**: Manage dishes/drinks with name, region, description, ingredients, difficulty, spicy level, vegetarian options, Amharic names, photos, and restaurant suggestions.
- **Random Suggestions**: `/recommendation/random`, `/foods/random`, `/drinks/random` for discovering new items.
- **Regional Recommendations**: `/recommendation/by-region/{region}` to explore cuisine by Ethiopian region.
- **Favorites & History**: Users can save favorites (`/favorites/{item_id}`) and track tried items (`/tried/{item_id}`), with retrieval endpoints (`/favorites`, `/tried`).
- **Cultural Trivia**: Fun facts about dishes/drinks (e.g., "Doro Wat is served during festivals").
- **Multi-Language**: Supports English and Amharic via `lang=am` query parameter.
- **Filters**: Vegetarian and spicy level filtering (`/foods?vegetarian=true&spicy_level=hot`), popularity sorting (`/foods/popular`, `/drinks/popular`).
- **Geolocation**: `/recommendation/nearby?lat={lat}&lon={lon}` suggests foods within 10km (requires lat/lon in restaurant data).
- **Rating System**: Rate foods/drinks (`/foods/{id}/rate`, `/drinks/{id}/rate`, 1-5 scale).
- **Social Sharing**: Generate shareable text (`/foods/{id}/share`, `/drinks/{id}/share`).
- **Daily Suggestion**: `/recommendation/daily` for a daily food/drink pick.
- **Quiz Mode**: `/foods/quiz` for an interactive ingredients-based quiz.
- **Authentication**: JWT-based user authentication for protected endpoints (`/users/login`, `/users`).

## Tech Stack
- **Framework**: FastAPI
- **Database**: MongoDB (via Motor for async operations)
- **Authentication**: JWT with bcrypt password hashing
- **Dependencies**: `fastapi`, `uvicorn`, `motor`, `pydantic`, `pymongo`, `python-dotenv`, `python-jose[cryptography]`, `passlib[bcrypt]`, `geopy`

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Injera-Beyond
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn motor pydantic pymongo python-dotenv python-jose[cryptography] passlib[bcrypt] geopy
   ```
4. Configure `.env`:
   ```
   MONGODB_URL=<your-mongodb-connection-string>
   SECRET_KEY=<your-secret-key>
   ```
5. Run the API:
   ```bash
   uvicorn main:app --reload
   ```
6. Access at `http://127.0.0.1:8000/docs` for Swagger UI.

## Endpoints
- **Foods**: `POST /foods`, `GET /foods`, `GET /foods/{id}`, `PUT /foods/{id}`, `DELETE /foods/{id}`, `GET /foods/random`, `GET /foods/quiz`, `POST /foods/{id}/rate`, `GET /foods/{id}/share`, `GET /foods/popular`
- **Drinks**: `POST /drinks`, `GET /drinks`, `GET /drinks/{id}`, `PUT /drinks/{id}`, `DELETE /drinks/{id}`, `GET /drinks/random`, `POST /drinks/{id}/rate`, `GET /drinks/{id}/share`, `GET /drinks/popular`
- **Users**: `POST /users`, `GET /users`, `POST /users/login`
- **Recommendations**: `GET /recommendation/random`, `GET /recommendation/by-region/{region}`, `GET /recommendation/daily`, `GET /recommendation/nearby`
- **Favorites**: `POST /favorites/{item_id}`, `POST /tried/{item_id}`, `GET /favorites`, `GET /tried`

## Notes
- **MongoDB**: Requires a valid MongoDB Atlas connection string.
- **Data**: Populate `foods` and `drinks` collections with sample data (e.g., Doro Wat, Tej) for testing.
- **Production**: Secure `SECRET_KEY`, adjust CORS origins, and add rate limiting.
- **Geolocation**: Assumes `restaurant_suggestions` format: "Name, City, Lat, Lon".

## License
MIT License

---

