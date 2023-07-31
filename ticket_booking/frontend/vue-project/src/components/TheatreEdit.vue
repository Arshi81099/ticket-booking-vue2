<template>
  <div class="edit-theatre-container">
    <h2>Edit Theatre Details</h2>
    <form @submit.prevent="editTheatre">
      <div class="form-group">
        <label for="name">Name:</label>
        <input v-model="name" type="text" id="name" required>
      </div>
      <div class="form-group">
        <label for="location">Capacity:</label>
        <input v-model="capacity" type="text" id="capacity" required>
      </div>
      <div class="form-group">
        <label for="contact">Address:</label>
        <input v-model="address" type="text" id="address" required>
      </div>
      <!-- <div class="form-group">
        <label for="code">Code:</label>
        <input v-model="code" type="text" id="code" required>
      </div> -->
      <button type="submit">Save</button>
    </form>
  </div>
</template>
  
<script>
export default {
  props: {
    theatre: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      name: null,
      capacity: null,
      address: null,
      // code: null,
    };
  },
  methods: {
    async editTheatre() {
      try {
        const theaterData = {
          name: this.name,
          capacity: this.capacity,
          address: this.address,
          // code: this.code,
        };
        const code = this.$route.params.theatreCode
        const response = await this.$http.put(`theatre/${code}`, theaterData);

        if (response.status === 201) {
          console.log("Theatre added successfully!");
          this.$router.push("/theatremanagement"); 
        } else {
          console.log(response.text);
        }
      } catch (error) {
        console.error("An error occurred:", error);
      }
    },
  },
  };
</script>
  
<style>
/* Custom Styles for the component */

.edit-theatre-container {
  margin: 20px;
  padding: 20px;
  border: 1px solid #000;
  background-color: pink;
  color: black;
  border-radius: 10px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  font-weight: bold;
  margin-right: 5px;
}

input {
  padding: 5px;
}

button {
  padding: 10px 20px;
  background-color: black;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #333;
}
</style>
  