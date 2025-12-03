# Rubik View - Stock Trading Platform

A full-stack stock trading platform with real-time data processing, indicator calculations, and AI-powered stock analysis.

## Project Structure

```
Rubik_view/
├── backend/          # FastAPI backend server
├── web_app/          # Next.js frontend application
├── Engine/           # Indicator processing engine
└── Data/             # All data files (databases, CSV files, etc.)
```

## Prerequisites

Before running the project, make sure you have installed:

- **Python 3.8+** (for backend)
- **Node.js 18+** (for frontend)
- **npm** or **yarn** (for frontend package management)

## Installation & Setup


Summary
Files to run:
Backend: backend/main.py (via uvicorn command)
Frontend: web_app directory (via npm run dev)
Commands:
Backend: python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Frontend: npm run dev

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or if you're using a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### 2. Frontend Setup

1. Navigate to the web_app directory:
   ```bash
   cd web_app
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

   Or using yarn:
   ```bash
   yarn install
   ```

## Running the Project

You need to run **both** the backend and frontend servers in separate terminals.

### Terminal 1: Start Backend Server

From the project root directory:

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will start on: **http://localhost:8000**

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Terminal 2: Start Frontend Server

From the project root directory:

```bash
cd web_app
npm run dev
```

The frontend will start on: **http://localhost:3000**

Open your browser and navigate to: **http://localhost:3000**

## Default Login Credentials

**Super Admin:**
- Email: `jallusandeep@rubikview.com`
- Password: `8686504620SAn@#1`

## Quick Start Commands

### Windows (PowerShell)

**Terminal 1 - Backend:**
```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```powershell
cd web_app
npm run dev
```

### Linux/Mac

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd web_app
npm run dev
```

## Project Components

### Backend (FastAPI)
- **Port:** 8000
- **Main File:** `backend/main.py`
- **API Base URL:** `http://localhost:8000/api/v1`
- **Features:**
  - User authentication (JWT tokens)
  - Stock data management
  - Indicator configuration
  - Job scheduling (OHCLV loading, Signal processing)
  - Admin console APIs

### Frontend (Next.js)
- **Port:** 3000
- **Main Directory:** `web_app/src/`
- **Features:**
  - User login/registration
  - Dashboard with stock analysis
  - Admin console
  - Real-time job monitoring
  - Indicator configuration UI

### Data Storage
- **User Database:** `Data/rubikview_users.db` (SQLite)
- **OHCLV Data:** `Data/OHCLV Data/stocks.duckdb` (DuckDB)
- **Signals Data:** `Data/Signals Data/signals.duckdb` (DuckDB)
- **Symbols Data:** `Data/Symbols Data/symbols.duckdb` (DuckDB)
- **Logs Database:** `Data/logs.db` (SQLite)

## Troubleshooting

### Backend won't start
- Make sure all Python dependencies are installed: `pip install -r backend/requirements.txt`
- Check if port 8000 is already in use
- Verify the database file exists: `Data/rubikview_users.db`

### Frontend won't start
- Make sure Node.js dependencies are installed: `npm install` in `web_app/` directory
- Check if port 3000 is already in use
- Clear Next.js cache: `rm -rf web_app/.next` (Linux/Mac) or `Remove-Item -Recurse -Force web_app\.next` (Windows)

### Database errors
- The database will be created automatically on first run
- Make sure the `Data/` folder exists
- Check file permissions on the database file

### Connection errors between frontend and backend
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify the API base URL in `web_app/src/lib/api.ts` is correct

## Development

### Backend Development
- Backend uses hot-reload with `--reload` flag
- Changes to Python files will automatically restart the server
- API documentation available at `/docs` when server is running

### Frontend Development
- Frontend uses Next.js hot-reload
- Changes to React/TypeScript files will automatically update in browser
- Check browser console for any errors

## Production Deployment

### Backend
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd web_app
npm run build
npm start
```

## Additional Notes

- The backend automatically creates database tables on startup
- Super admin user is created automatically if it doesn't exist
- Job scheduler is initialized on backend startup
- All data files are stored in the `Data/` folder

## Support

For issues or questions, please check the project repository or contact the development team.

