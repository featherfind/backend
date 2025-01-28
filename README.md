# FeatherFind Backend

This is the backend for FeatherFind, built using Django and Django Rest Framework (DRF).

## How to Run

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone git@github.com:featherfind/backend.git
```

### 2. Navigate to the Project Directory

```bash
cd backend
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate the Virtual Environment

**For Linux and Mac:**
```bash
source venv/bin/activate
```

**For Windows:**
```bash
.\venv\Scripts\activate.bat
```

### 5. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Project

```bash
python manage.py runserver
```

## API Endpoints

**HOST**: `http://localhost:8000`

### Birds

#### **GET /birds/**
Retrieve a list of all bird species.

- **Response:**

  ```json
  [
    {
      "id": 1,
      "name": "Satyr Tragopan",
      "species": "Tragopan satyra",
      "habitat": null,
      "background": "A brightly colored pheasant species, with striking red and orange plumage. Found in the dense forests of the western Himalayas.",
      "population_trend": "decreasing",
      "upper_elevation_limit": null,
      "lower_elevation_limit": null,
      "url": "https://en.wikipedia.org/wiki/Satyr_tragopan",
      "birdsets": [
        {
          "id": 1,
          "bird": 1,
          "image": "/media/images/8661673.jpg",
          "audio": null
        }
      ]
    }
  ]
  ```

#### **GET /birds/<int:bird_id>/**
Retrieve details of a specific bird species by its ID.

- **Request:**

  ```
  GET /birds/1/
  ```

- **Response:**

  ```json
  {
    "id": 1,
    "name": "Satyr Tragopan",
    "species": "Tragopan satyra",
    "habitat": null,
    "background": "A brightly colored pheasant species, with striking red and orange plumage. Found in the dense forests of the western Himalayas.",
    "population_trend": "decreasing",
    "upper_elevation_limit": null,
    "lower_elevation_limit": null,
    "url": "https://en.wikipedia.org/wiki/Satyr_tragopan",
    "birdsets": [
      {
        "id": 1,
        "bird": 1,
        "image": "/media/images/8661673.jpg",
        "audio": null
      }
    ]
  }
  ```

#### **GET /birds/assets/<int:bird_id>/**
Retrieve media assets (images and audio) for a specific bird by its ID.

- **Request:**

  ```
  GET /birds/assets/1/
  ```

- **Response:**

  ```json
  {
    "id": 1,
    "bird": 1,
    "image": "/media/images/8661673.jpg",
    "audio": null
  }
  ```

### Predict

#### **POST /birds/predict/**
Predict the bird species from audio input.

- **Request:**

  ```json
  {
    "audio": "<AUDIO_FILE_IN_BYTES>"
  }
  ```

- **Response:**

  ```json
  {
    "has_bird": true,
    "bird_id": 1,
    "confidence": 76,
    "image": "/media/images/15232321.jpg",
    "wiki-url": "https://wikipedia.org/example_bird_species"
  }
  ```

### Location

#### **GET /locations/bird/**
Retrieve a list of all mapped bird locations.

- **Request:**

  ```
  GET /locations/bird/
  ```

- **Response:**

  ```json
  [
    {
      "id": 1,
      "location": {
        "id": 1,
        "name": "",
        "latitude": "27.691667400000000",
        "longitude": "85.329765100000000",
        "description": null,
        "altitude": null,
        "habitat": null,
        "place_type": ""
      },
      "bird": {
        "id": 25,
        "name": "Eastern Imperial Eagle",
        "species": "Aquila heliaca",
        "habitat": null,
        "background": "A large eagle with powerful wings, found in grasslands and wetlands across Central Asia and Eastern Europe.",
        "population_trend": "decreasing",
        "upper_elevation_limit": null,
        "lower_elevation_limit": null,
        "url": "https://en.wikipedia.org/wiki/Eastern_imperial_eagle",
        "birdsets": [
          {
            "id": 26,
            "bird": 25,
            "image": "/media/images/images-15.jpeg",
            "audio": null
          }
        ]
      },
      "spotted_time": "2025-01-04T23:49:41.292000Z"
    }
  ]
  ```

#### **GET /locations/bird/<int:bird_id>/**
Retrieve all locations of a specific bird by its ID.

- **Request:**

  ```
  GET /locations/bird/25/
  ```

- **Response:**

  ```json
  [
    {
      "id": 1,
      "location": {
        "id": 1,
        "name": "",
        "latitude": "27.691667400000000",
        "longitude": "85.329765100000000",
        "description": null,
        "altitude": null,
        "habitat": null,
        "place_type": ""
      },
      "bird": {
        "id": 25,
        "name": "Eastern Imperial Eagle",
        "species": "Aquila heliaca",
        "habitat": null,
        "background": "A large eagle with powerful wings, found in grasslands and wetlands across Central Asia and Eastern Europe.",
        "population_trend": "decreasing",
        "upper_elevation_limit": null,
        "lower_elevation_limit": null,
        "url": "https://en.wikipedia.org/wiki/Eastern_imperial_eagle",
        "birdsets": [
          {
            "id": 26,
            "bird": 25,
            "image": "/media/images/images-15.jpeg",
            "audio": null
          }
        ]
      },
      "spotted_time": "2025-01-04T23:49:41.292000Z"
    }
  ]
  ```

#### **POST /locations/birds/<int:bird_id>/**
Map a bird to a specific location.

- **Request:**

  ```json
  {
    "latitude": 25.22,
    "longitude": 20.22,
    "timestamp": "2025-01-28 06:00:23"
  }
  ```

- **Response:**

  ```json
  {
    "id": 31,
    "location": {
      "id": 31,
      "name": "",
      "latitude": "27.688790470968000",
      "longitude": "85.328093995729300",
      "description": null,
      "altitude": null,
      "habitat": null,
      "place_type": ""
    },
    "bird": {
      "id": 25,
      "name": "Eastern Imperial Eagle",
      "species": "Aquila heliaca",
      "habitat": null,
      "background": "A large eagle with powerful wings, found in grasslands and wetlands across Central Asia and Eastern Europe.",
      "population_trend": "decreasing",
      "upper_elevation_limit": null,
      "lower_elevation_limit": null,
      "url": "https://en.wikipedia.org/wiki/Eastern_imperial_eagle",
      "birdsets": [
        {
          "id": 26,
          "bird": 25,
          "image": "/media/images/images-15.jpeg",
          "audio": null
        }
      ]
    },
    "spotted_time": "2025-01-05T03:24:30.944000Z"
  }
  ```

