<template>
    <div>
      <!-- Display the list of movies -->
      <h2>Movie List</h2>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Genre</th>
            <th>Duration</th>
            <th>Synopsis</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="movie in movies" :key="movie.id">
            <td>{{ movie.title }}</td>
            <td>{{ movie.genre }}</td>
            <td>{{ movie.duration }}</td>
            <td>{{ movie.synopsis }}</td>
            <td>
              <button @click="editMovie(movie)">Edit</button>
              <button @click="deleteMovie(movie.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Form to add/edit movie -->
      <h2>{{ isEditMode ? 'Edit Movie' : 'Add Movie' }}</h2>
      <form @submit.prevent="saveMovie">
        <input v-model="formData.title" type="text" placeholder="Title" required>
        <input v-model="formData.genre" type="text" placeholder="Genre" required>
        <input v-model="formData.duration" type="text" placeholder="Duration" required>
        <textarea v-model="formData.synopsis" placeholder="Synopsis" required></textarea>
        <input type="file" @change="handleFileChange" accept="image/*" />
        <button type="submit">{{ isEditMode ? 'Save' : 'Add' }}</button>
        <button type="button" @click="cancelEdit">Cancel</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        movies: [
          // Sample data, replace with actual movie data from API or database
          {
            id: 1,
            title: 'Movie 1',
            genre: 'Action',
            duration: '2h 30min',
            synopsis: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
          },
          {
            id: 2,
            title: 'Movie 2',
            genre: 'Comedy',
            duration: '1h 45min',
            synopsis: 'Pellentesque vitae odio vitae lorem ultricies bibendum.',
          },
          // Add more movies here
        ],
        formData: {
          title: '',
          genre: '',
          duration: '',
          synopsis: '',
          posterImage: null,
        },
        isEditMode: false,
      };
    },
    methods: {
      saveMovie() {
        if (this.isEditMode) {
          // Handle edit movie logic here
          // Update the movie details in the movies array based on the formData
          // This is just a placeholder code
          alert('Movie updated!');
        } else {
          // Handle add movie logic here
          // Add the new movie details to the movies array based on the formData
          // This is just a placeholder code
          const newMovie = {
            id: this.movies.length + 1,
            title: this.formData.title,
            genre: this.formData.genre,
            duration: this.formData.duration,
            synopsis: this.formData.synopsis,
          };
          this.movies.push(newMovie);
          alert('Movie added!');
        }
        // Reset the form data and exit edit mode
        this.resetForm();
      },
      editMovie(movie) {
        // Set the form data to the selected movie for editing
        this.formData.title = movie.title;
        this.formData.genre = movie.genre;
        this.formData.duration = movie.duration;
        this.formData.synopsis = movie.synopsis;
        this.isEditMode = true;
      },
      deleteMovie(id) {
        // Handle delete movie logic here
        // Remove the movie from the movies array based on the given id
        // This is just a placeholder code
        this.movies = this.movies.filter((movie) => movie.id !== id);
        alert('Movie deleted!');
      },
      handleFileChange(event) {
        // Handle file input change to get the selected poster image
        this.formData.posterImage = event.target.files[0];
      },
      cancelEdit() {
        // Reset the form data and exit edit mode
        this.resetForm();
      },
      resetForm() {
        // Reset the form data and exit edit mode
        this.formData.title = '';
        this.formData.genre = '';
        this.formData.duration = '';
        this.formData.synopsis = '';
        this.formData.posterImage = null;
        this.isEditMode = false;
      },
    },
  };
  </script>
  
  <style>
  /* Add custom styles for the MovieManagement component */
  /* Styles for the table */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  th,
  td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ccc;
  }
  
  th {
    background-color: #f9f9f9;
  }
  
  /* Styles for the form */
  form {
    display: flex;
    flex-direction: column;
    max-width: 400px;
    margin-bottom: 20px;
  }
  
  input[type="text"],
  textarea {
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  input[type="file"] {
    display: none;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  button {
    padding: 10px 20px;
    background-color: #ff69b4;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button[type="submit"] {
    background-color: #ff69b4;
  }
  
  button[type="button"] {
    background-color: #ccc;
  }
  
  /* Styles for the table container */
  .movie-list {
    max-height: 300px;
    overflow-y: auto;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  /* Styles for the edit button */
  .edit-button {
    background-color: #ffc107;
    color: #fff;
  }
  
  /* Styles for the delete button */
  .delete-button {
    background-color: #dc3545;
    color: #fff;
  }
  
  /* Styles for the cancel button */
  .cancel-button {
    background-color: #6c757d;
    color: #fff;
  }
  </style>
  