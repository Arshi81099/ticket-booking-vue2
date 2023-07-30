<template>
  <div class="movie-details">
    <h2>{{ movie.title }}</h2>
    <p>Genre: {{ movie.genre }}</p>
    <p>Duration: {{ movie.duration }} minutes</p>
    <p>Synopsis: {{ movie.synopsis }}</p>
    <!-- Embed the trailer using an iframe -->
    <iframe width="560" height="315" :src="movie.trailer" frameborder="0" allowfullscreen></iframe>

    <h3>Available Showtimes and Theatres</h3>
    <ul>
      <li v-for="showtime in availableShowtimes" :key="showtime.id">
        {{ showtime.date }} at {{ showtime.time }} - {{ showtime.theatreName }}
        <button @click="bookTicket(showtime.id)">Book Tickets</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    movie: {
      type: Object,
      required: true,
    },
    availableShowtimes: {
      type: Array,
      required: true,
    },
  },
  methods: {
    bookTicket(showtimeId) {
      // Handle ticket booking logic here
      // For example, navigate to a booking page or show a booking dialog
      // You can also pass the selected showtimeId to the booking page or dialog
    },
  },
};
</script>

<style>
/* Add custom styles for the MovieDetails component */

.movie-details {
  /* Add overall styles for the movie details section */
  padding: 20px;
}

.movie-title {
  /* Style for the movie title */
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.movie-genre {
  /* Style for the movie genre */
  font-size: 16px;
  color: #666;
}

.movie-duration {
  /* Style for the movie duration */
  font-size: 16px;
  color: #666;
}

.movie-synopsis {
  /* Style for the movie synopsis */
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.showtimes-heading {
  /* Style for the showtimes heading */
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.showtimes-list {
  /* Style for the list of showtimes */
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.showtime-item {
  /* Style for each showtime item */
  margin-bottom: 10px;
  font-size: 16px;
  color: #666;
}

.book-ticket-btn {
  /* Style for the "Book Tickets" button */
  background-color: #ff69b4;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.book-ticket-btn:hover {
  /* Style for the "Book Tickets" button on hover */
  background-color: #ff5080;
}
</style>








  
  