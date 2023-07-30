<template>
    <div class="landing-page h-100">

      <!-- Header section -->
      <header class="w-100">

        <nav>
        </nav>
      </header>  
      <ImageSlider />
      <!-- Hero section -->
      <section class="hero">
        <div class="hero-content">
          <h1>Welcome to Movie Ticket Booking</h1>
          <p>Book your favorite movies in just a few clicks!</p>
          <!-- You can add a button to navigate to the movie listing page -->
          <router-link to="/movies" class="btn btn-primary">Explore Movies</router-link>

        </div>
      </section>
      <div class="home-page">
    <div class="featured-movies">
      <h2>Featured Movies</h2>
      <div class="movie-carousel">
        <div v-for="movie in featuredMovies" :key="movie.id" class="movie-card">
          <img :src="movie.poster" alt="Movie Poster">
          <h3>{{ movie.title }}</h3>
          <p>{{ movie.genre }}</p>
          <!-- Add other movie details as needed -->
        </div>
      </div>
    </div>
    <div class="upcoming-events">
      <h2>Upcoming Events</h2>
      <div class="event-carousel">
        <div v-for="event in upcomingEvents" :key="event.id" class="event-card">
          <img :src="event.image" alt="Event Image">
          <h3>{{ event.title }}</h3>
          <p>{{ event.date }}</p>
          <!-- Add other event details as needed -->
        </div>
      </div>
    </div>
    <div class="search-bar">
      <v-text-field
        v-model="searchQuery"
        append-icon="search"
        label="Search for movies, theatres, or events"
        hide-details
      ></v-text-field>
    </div>
    <div class="filter-options">
      <!-- Add filter options here, such as dropdowns, checkboxes, etc. -->
      <!-- For simplicity, we'll just use a select dropdown as an example -->
      <v-select
        v-model="selectedGenre"
        :items="genres"
        label="Filter by Genre"
        hide-details
      ></v-select>
    </div>
      <!-- Footer section -->
      <footer>
        <!-- Your footer content can go here -->
      </footer>
    </div>
    </div>
  </template>
  
  <script>
  import BootstrapVue from 'bootstrap-vue';
  import 'bootstrap/dist/css/bootstrap.css';
  import 'bootstrap-vue/dist/bootstrap-vue.css';
  import ImageSlider from '../components/ImageSlider.vue'; 
  import NavBar from '../components/NavBar.vue';

  
  export default {
    name: 'LandingPage',
    components: {
      BootstrapVue,
      ImageSlider,
      NavBar,
    },
    data() {
    return {
      featuredMovies: [
        {
          id: 1,
          title: "Movie 1",
          genre: "Action",
          poster: "/Users/arshi/Desktop/ticket_booking/frontend/vue-project/src/assets/movie1.jpeg",
        },
        // Add more featured movies here
      ],
      upcomingEvents: [
        {
          id: 1,
          title: "Event 1",
          date: "2023-07-31",
          image: "/Users/arshi/Desktop/ticket_booking/frontend/vue-project/src/assets/movie2.jpeg",
        },
        // Add more upcoming events here
      ],
      searchQuery: '',
      selectedGenre: null,
      featuredMovies: [
        // Featured movies data (same as before)
      ],
      upcomingEvents: [
        // Upcoming events data (same as before)
      ],
      genres: [
        'Action',
        'Comedy',
        'Drama',
        'Sci-Fi',
        // Add more genres as needed
      ],
    };
  },
  };
  </script>
  
  <style>
  /* Add specific styles for the landing page */
  
  .landing-page {
    /* Overall styles for the landing page container */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f9f9f9;
    /* padding: 2rem; */
  }
  
  .hero {
    /* Styles for the hero section */
    text-align: center;
  }
  
  .hero-content {
    /* Styles for the content within the hero section */
    max-width: 500px;
  }
  
  .hero h1 {
    font-size: 36px;
    margin-bottom: 1rem;
    color: #333;
  }
  
  .hero p {
    font-size: 18px;
    color: #666;
    margin-bottom: 2rem;
  }
  
  .hero .btn-primary {
    /* Styles for the primary button */
    background-color: #ff69b4;
  }

  /* Styles for the carousel */
.carousel-container {
  max-width: 800px; /* Set the maximum width of the carousel */
  margin: 0 auto; /* Center the carousel horizontally */
}

.carousel-slide {
  /* Set the height of the carousel slides */
  height: 400px;
}

.carousel-slide img {
  /* Set the width and height of the carousel images */
  width: 100%;
  height: 100%;
  object-fit: cover; /* Preserve aspect ratio of images */
  border-radius: 8px; /* Optional: Add border-radius for rounded corners */
}
.image-overlay {
  width: 100px;
  height: 100px;
  position: absolute;
  background-color: #f85752;
  opacity: 0.5;
}
  /* Add any other specific styles for the landing page components */
  .movie-carousel {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.movie-card {
  margin: 20px;
  text-align: center;
}

.movie-card img {
  width: 200px;
  height: 300px;
  object-fit: cover;
}

.event-carousel {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.event-card {
  margin: 20px;
  text-align: center;
}

.event-card img {
  width: 200px;
  height: 150px;
  object-fit: cover;
}

.search-bar {
  margin: 20px auto;
  max-width: 500px;
}

.filter-options {
  margin: 20px auto;
  max-width: 500px;
}

/* Add styles for the select dropdown */
.v-select {
  width: 100%;
}
  </style>
  