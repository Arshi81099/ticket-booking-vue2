<template>
    <div class="theatre-details">
      <h2 class="theatre-name">{{ theatre.name }}</h2>
      <p class="theatre-location">Location: {{ theatre.location }}</p>
      <p class="theatre-address">Address: {{ theatre.address }}</p>
      <p class="theatre-contact">Contact: {{ theatre.contact }}</p>
      <p class="theatre-facilities">Facilities: {{ theatre.facilities.join(', ') }}</p>
  
      <h3 class="movies-heading">Movies and Showtimes</h3>
      <ul class="movies-list">
        <li v-for="movie in movies" :key="movie.id" class="movie-item">
          <div class="movie-details">
            <h4 class="movie-title">{{ movie.title }}</h4>
            <p class="movie-genre">Genre: {{ movie.genre }}</p>
            <p class="movie-duration">Duration: {{ movie.duration }} minutes</p>
            <p class="movie-synopsis">Synopsis: {{ movie.synopsis }}</p>
          </div>
          <div class="showtimes">
            <h4 class="showtimes-heading">Showtimes</h4>
            <ul class="showtimes-list">
              <li v-for="showtime in movie.showtimes" :key="showtime.id" class="showtime-item">
                {{ showtime.date }} at {{ showtime.time }}
                <button @click="bookTicket(movie.id, showtime.id)" class="book-ticket-btn">Book Tickets</button>
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      theatre: {
        // type: Object,
        // required: true,
        
      },
      movies: {
        // type: Array,
        // required: true,
      },
    },
    methods: {
      bookTicket(movieId, showtimeId) {
        // Handle ticket booking logic here
        // For example, navigate to a booking page or show a booking dialog
        // You can also pass the selected movieId and showtimeId to the booking page or dialog
        alert(`Booking tickets for Movie ID: ${movieId} and Showtime ID: ${showtimeId}`);
      },
    },
  };
  </script>
  
  <style>
  /* Custom Styles for the TheatreDetails component */
  
  .theatre-details {
    padding: 20px;
    background-color: pink;
    color: black;
  }
  
  .theatre-name {
    font-size: 24px;
    font-weight: bold;
  }
  
  .theatre-location,
  .theatre-address,
  .theatre-contact,
  .theatre-facilities {
    font-size: 16px;
  }
  
  .movies-heading {
    font-size: 20px;
    font-weight: bold;
  }
  
  .movies-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  .movie-item {
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 10px;
  }
  
  .movie-title {
    font-size: 18px;
    font-weight: bold;
  }
  
  .movie-genre,
  .movie-duration,
  .movie-synopsis {
    font-size: 16px;
    margin-bottom: 5px;
  }
  
  .showtimes {
    margin-top: 10px;
  }
  
  .showtimes-heading {
    font-size: 16px;
    font-weight: bold;
  }
  
  .showtimes-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  .showtime-item {
    font-size: 14px;
    margin-bottom: 5px;
  }
  
  .book-ticket-btn {
    background-color: black;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .book-ticket-btn:hover {
    background-color: #333;
  }
  </style>
  