# ALX Travel App - Backend (0x01)

A comprehensive Django REST API for a travel booking platform that allows users to search, book, and review accommodations worldwide. This version includes fully functional CRUD API endpoints with Swagger documentation.

## 🚀 Features

- **Accommodation Listings**: Browse and manage property listings
- **Booking System**: Complete booking workflow with validations
- **Review System**: User reviews and ratings for properties
- **REST API**: Full API with Swagger documentation
- **Background Tasks**: Celery integration for async processing
- **Admin Interface**: Django admin for content management

## 🛠️ Technologies Used

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production ready)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Task Queue**: Celery with Redis
- **Cross-Origin**: django-cors-headers
- **Media Processing**: Pillow for image handling

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Redis (for Celery tasks)
- Git

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/alx_travel_app_0x00.git
cd alx_travel_app_0x00/alx_travel_app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Seed Database (Optional)
```bash
python manage.py seed
# Or with custom counts
python manage.py seed --listings 20 --bookings 50 --reviews 30
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🏗️ Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app               
├── alx_travel_app/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py            # Celery configuration
├── listings/
│   ├── __init__.py
│   ├── models.py            # Database models (Listing, Booking, Review)
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── urls.py              # Listings URL patterns
│   ├── admin.py             # Django admin configuration
│   ├── management/
│   │   └── commands/
│   │       └── seed.py      # Database seeding command
│   └── migrations/
├── media/                   # User uploaded files
├── static/                  # Static files
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
├── .gitignore
└── README.md
```

## 🗄️ Database Models

### Listing
- Property details (title, description, location)
- Pricing and capacity information
- Host relationship
- Availability status

### Booking
- Booking details (dates, guests, pricing)
- User and listing relationships
- Status tracking (pending, confirmed, cancelled, completed)

### Review
- User reviews and ratings (1-5 stars)
- Review content and timestamps
- Linked to specific listings

## 🔧 Management Commands

### Database Seeding
```bash
# Seed with default data
python manage.py seed

# Custom data amounts
python manage.py seed --listings 15 --bookings 30 --reviews 25
```

## 🚀 Deployment

### Environment Variables
Set these in production:
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
CELERY_BROKER_URL=redis://redis-server:6379/0
```

### Static Files
```bash
python manage.py collectstatic
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test listings
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 API Endpoints

### Listings API

#### Standard CRUD Operations
- **GET** `/api/listings/` - List all listings
  - Query Parameters: `location`, `is_available`, `bedrooms`, `bathrooms`, `search`, `ordering`
  - Example: `/api/listings/?location=Paris&bedrooms=2&ordering=-price_per_night`

- **POST** `/api/listings/` - Create a new listing (Authentication required)
  - Request Body:
    ```json
    {
      "title": "Cozy Apartment in Paris",
      "description": "Beautiful apartment with Eiffel Tower view",
      "location": "Paris, France",
      "price_per_night": 150.00,
      "bedrooms": 2,
      "bathrooms": 1,
      "max_guests": 4,
      "is_available": true
    }
    ```

- **GET** `/api/listings/{id}/` - Get specific listing details
- **PUT** `/api/listings/{id}/` - Update entire listing (Authentication required)
- **PATCH** `/api/listings/{id}/` - Partially update listing (Authentication required)
- **DELETE** `/api/listings/{id}/` - Delete listing (Authentication required)

#### Custom Actions
- **GET** `/api/listings/available/` - Get only available listings
- **GET** `/api/listings/{id}/bookings/` - Get all bookings for a specific listing

### Bookings API

#### Standard CRUD Operations
- **GET** `/api/bookings/` - List all bookings (filtered by authenticated user)
  - Query Parameters: `status`, `listing`, `ordering`
  - Example: `/api/bookings/?status=confirmed&ordering=-created_at`

- **POST** `/api/bookings/` - Create a new booking (Authentication required)
  - Request Body:
    ```json
    {
      "listing": "uuid-of-listing",
      "check_in_date": "2025-10-15",
      "check_out_date": "2025-10-20",
      "number_of_guests": 2,
      "total_price": 750.00
    }
    ```

- **GET** `/api/bookings/{id}/` - Get specific booking details
- **PUT** `/api/bookings/{id}/` - Update entire booking
- **PATCH** `/api/bookings/{id}/` - Partially update booking
- **DELETE** `/api/bookings/{id}/` - Cancel/delete booking

#### Custom Actions
- **POST** `/api/bookings/{id}/cancel/` - Cancel a booking
- **POST** `/api/bookings/{id}/confirm/` - Confirm a booking (Host only)
- **GET** `/api/bookings/my_bookings/` - Get current user's bookings

## 🧪 Testing API Endpoints with Postman

### Setup
1. Download and install [Postman](https://www.postman.com/downloads/)
2. Start your Django development server: `python manage.py runserver`
3. Create a superuser if you haven't: `python manage.py createsuperuser`

### Testing Workflow

#### 1. Test GET Listings
```
Method: GET
URL: http://127.0.0.1:8000/api/listings/
Headers: None required
Expected: 200 OK with list of listings
```

#### 2. Test POST Create Listing (Requires Authentication)
```
Method: POST
URL: http://127.0.0.1:8000/api/listings/
Headers: 
  - Content-Type: application/json
Auth: Basic Auth (username/password from createsuperuser)
Body (raw JSON):
{
  "title": "Luxury Villa in Bali",
  "description": "Amazing villa with private pool",
  "location": "Bali, Indonesia",
  "price_per_night": 250.00,
  "bedrooms": 3,
  "bathrooms": 2,
  "max_guests": 6,
  "is_available": true
}
Expected: 201 Created
```

#### 3. Test GET Single Listing
```
Method: GET
URL: http://127.0.0.1:8000/api/listings/{listing_id}/
Expected: 200 OK with listing details
```

#### 4. Test PUT Update Listing
```
Method: PUT
URL: http://127.0.0.1:8000/api/listings/{listing_id}/
Auth: Basic Auth
Body: Complete listing object with updates
Expected: 200 OK
```

#### 5. Test PATCH Partial Update
```
Method: PATCH
URL: http://127.0.0.1:8000/api/listings/{listing_id}/
Auth: Basic Auth
Body (raw JSON):
{
  "price_per_night": 275.00,
  "is_available": false
}
Expected: 200 OK
```

#### 6. Test POST Create Booking
```
Method: POST
URL: http://127.0.0.1:8000/api/bookings/
Auth: Basic Auth
Body (raw JSON):
{
  "listing": "{listing_uuid}",
  "check_in_date": "2025-11-01",
  "check_out_date": "2025-11-05",
  "number_of_guests": 2,
  "total_price": 1000.00
}
Expected: 201 Created
```

#### 7. Test Custom Actions
```
# Cancel Booking
Method: POST
URL: http://127.0.0.1:8000/api/bookings/{booking_id}/cancel/
Auth: Basic Auth
Expected: 200 OK

# Get Available Listings
Method: GET
URL: http://127.0.0.1:8000/api/listings/available/
Expected: 200 OK

# Get My Bookings
Method: GET
URL: http://127.0.0.1:8000/api/bookings/my_bookings/
Auth: Basic Auth
Expected: 200 OK
```

#### 8. Test Filtering and Search
```
# Filter by location
GET http://127.0.0.1:8000/api/listings/?location=Paris

# Search in title/description
GET http://127.0.0.1:8000/api/listings/?search=luxury

# Order by price
GET http://127.0.0.1:8000/api/listings/?ordering=price_per_night

# Combine filters
GET http://127.0.0.1:8000/api/listings/?location=Bali&bedrooms=3&ordering=-price_per_night
```

#### 9. Test DELETE
```
Method: DELETE
URL: http://127.0.0.1:8000/api/listings/{listing_id}/
Auth: Basic Auth
Expected: 204 No Content
```

### Expected Response Codes
- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation errors
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource doesn't exist

### Testing Error Scenarios

1. **Missing Required Fields**
   - Try creating a listing without required fields
   - Expected: 400 Bad Request with error details

2. **Invalid Data Types**
   - Send string for numeric field
   - Expected: 400 Bad Request

3. **Unauthorized Access**
   - Try POST/PUT/DELETE without authentication
   - Expected: 401 Unauthorized

4. **Invalid UUID**
   - Use invalid listing_id
   - Expected: 404 Not Found

## 🐛 Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Make sure Redis is running: `redis-server`
   - Check CELERY_BROKER_URL in settings

2. **Migration Issues**
   - Delete migration files and remake: `python manage.py makemigrations`
   - Reset database: `python manage.py flush`

3. **Static Files Not Loading**
   - Run: `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT settings

## 📄 License

This project is part of the ALX Software Engineering program.

## 👥 Authors

- Your Name - [@your-github-username](https://github.com/your-github-username)

## 🙏 Acknowledgments

- ALX Software Engineering Program
- Django and DRF communities
- Contributors and reviewers