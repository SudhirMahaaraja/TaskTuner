# TaskTuner

**Smart Task Scheduling Made Simple**

TaskTuner is a Flask-based web application that transforms your productivity by intelligently scheduling tasks. Import tasks from Trello, set effort estimates, and let advanced algorithms create the perfect daily schedule for you.

## Features

- 🎯 **Smart Scheduling** - Advanced algorithms optimize your daily schedule based on task effort and priorities
- 📊 **Trello Integration** - Seamlessly import tasks from your Trello boards with real-time synchronization
- ⚡ **Effort Tracking** - Set realistic time estimates and track your progress with intuitive interfaces
- 📅 **Visual Calendar** - Interactive calendar view powered by FullCalendar
- 🔄 **Multiple Algorithms** - Choose between balanced, largest-first, or smallest-first scheduling strategies

## Quick Start

### Prerequisites

- Python 3.7+
- Trello account and API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tasktuner.git
   cd tasktuner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Trello credentials
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Trello Setup

### Getting Your Trello API Credentials

1. **Get your Trello API Key**
   - Visit [https://trello.com/app-key](https://trello.com/app-key)
   - Copy your API Key

2. **Generate a Token**
   - Click on the "Token" link on the same page
   - Authorize the application
   - Copy your Token

3. **Find Your Board ID (Optional)**
   - Open your Trello board in a browser
   - The URL will look like: `https://trello.com/b/BOARD_ID/board-name`
   - Copy the `BOARD_ID` part

### Environment Configuration

Create a `.env` file in the root directory:

```env
# Required
TRELLO_KEY=your_trello_api_key_here
TRELLO_TOKEN=your_trello_token_here

# Optional
BOARD_ID=your_board_id_here
DAILY_HOUR_LIMIT=8
SECRET_KEY=your_secret_key_here
```

**Environment Variables:**
- `TRELLO_KEY` - Your Trello API key (required)
- `TRELLO_TOKEN` - Your Trello API token (required)
- `BOARD_ID` - Specific board ID to fetch tasks from (optional, defaults to all your cards)
- `DAILY_HOUR_LIMIT` - Maximum hours per day for scheduling (default: 8)
- `SECRET_KEY` - Flask session secret (optional, has fallback)

## Project Structure

```
tasktuner/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
├── controllers/         # Route controllers
│   ├── page_controller.py    # UI routes
│   ├── task_controller.py    # Task API routes
│   └── schedule_controller.py # Schedule API routes
├── models/              # Data models
│   ├── task.py          # Task model with persistence
│   └── schedule.py      # Schedule model
├── services/            # Business logic
│   ├── trello_service.py     # Trello API integration
│   ├── scheduling.py         # Scheduling algorithms
│   └── asana_service.py      # (Placeholder for future)
├── views/               # Templates and static files
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── tasks.html
│       └── schedule.html
└── tests/               # Test files
```

## Usage

### 1. Home Page
- Overview of features and navigation
- Access to Tasks and Schedule views

### 2. Tasks Management (`/tasks-ui`)
- View all imported Trello tasks
- Set effort estimates (in hours) for each task
- Bulk edit multiple tasks at once
- Save changes with visual confirmation

### 3. Schedule View (`/schedule-ui`)
- Interactive calendar showing scheduled tasks
- Choose scheduling algorithm:
  - **Balanced**: Maintains original task order
  - **Largest First**: Schedules high-effort tasks first
  - **Smallest First**: Schedules low-effort tasks first
- Drag and drop tasks to reschedule
- Real-time statistics

## API Documentation

### Tasks API

#### Get All Tasks
```http
GET /tasks
```
Fetches and syncs tasks from Trello, returns all tasks with effort estimates.

**Response:**
```json
[
  {
    "id": "trello_card_id",
    "name": "Task name",
    "effort": 5
  }
]
```

#### Update Task Effort
```http
POST /tasks/effort
Content-Type: application/json
```

**Single task:**
```json
{
  "taskId": "trello_card_id",
  "hours": 3
}
```

**Multiple tasks:**
```json
[
  {"taskId": "id1", "hours": 2},
  {"taskId": "id2", "hours": 4}
]
```

### Schedule API

#### Generate Schedule
```http
GET /schedule?startDate=2025-01-01&alg=balanced
```

**Parameters:**
- `startDate` (optional): Start date in YYYY-MM-DD format
- `alg` (optional): Algorithm - `balanced`, `largest`, or `smallest`

**Response:**
```json
[
  {
    "date": "2025-01-01",
    "tasks": [
      {
        "id": "task_id",
        "name": "Task name",
        "effort": 3
      }
    ]
  }
]
```

## Scheduling Algorithms

### Balanced (Default)
Maintains the original order of tasks while respecting daily hour limits. Tasks are split across days if they exceed the daily limit.

### Largest First
Sorts tasks by effort in descending order, scheduling the most time-consuming tasks first. Good for tackling big items early.

### Smallest First
Sorts tasks by effort in ascending order, scheduling quick wins first. Good for building momentum.

## Development

### Running Tests
```bash
pytest
```

### Development Mode
The application runs with `use_reloader=False` to maintain in-memory state during development.

### Data Persistence
Task data is automatically saved to `tasks_store.json` for persistence between sessions.

## Troubleshooting

### Trello Connection Issues
- Verify your API key and token are correct
- Check that your token has the necessary permissions
- If using `BOARD_ID`, ensure it's the correct ID from the URL

### Local Fallback
If Trello API is unavailable, the app will attempt to load tasks from `task_data.json` as a fallback.

### Common Issues
- **Empty task list**: Check your Trello credentials and board access
- **Schedule not generating**: Ensure tasks have effort estimates > 0
- **Calendar not loading**: Check browser console for JavaScript errors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Asana integration
- [ ] Task priority levels
- [ ] Recurring task support
- [ ] Team collaboration features
- [ ] Mobile app
- [ ] Export to external calendars

## Support

For questions and support, please open an issue on GitHub or contact the maintainers.