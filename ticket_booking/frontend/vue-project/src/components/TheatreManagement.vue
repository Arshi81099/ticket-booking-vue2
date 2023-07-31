<template>
  <div>
    <!-- Add Theatre button -->
    <button @click="seeStatus">Add Theatre</button>

    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Capacity</th>
          <th>Address</th>
          <th>Code</th>
          <th>Edit/Delete</th>
        </tr>
      </thead>
      <!-- Table Body -->
      <tbody>
        <tr v-for="(theatre, index) in theatres" :key="index">
          <td>{{ theatre.name }}</td>
          <td>{{ theatre.capacity }}</td>
          <td>{{ theatre.address }}</td>
          <td>{{ theatre.code }}</td>
          <td>
            <button @click="editTheatre(theatre.code)">Edit</button>
            <button @click="deleteTheatre(theatre.code)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div>
    <!-- Your button -->
    <button @click="toggleDivVisibility">Toggle Div</button>

    <!-- The div to be shown/hidden -->
    <div v-if="isDivVisible">
      <!-- Content of the div -->
      <p>This is the hidden div.</p>
    </div>
  </div>

    <!-- Add Theatre Form -->
    <form v-if="currentStatus" @submit.prevent="saveTheatre">
      <!-- Form Fields -->
      <label for="name">Theatre Name:</label>
      <input type="text" v-model="newTheatre.name" id="name" required>

      <label for="capacity">Capacity:</label>
      <input type="number" v-model="newTheatre.capacity" id="capacity" required>

      <label for="address">Address:</label>
      <input type="text" v-model="newTheatre.address" id="address" required>

      <label for="code">Theatre Code:</label>
      <input type="text" v-model="newTheatre.code" id="code" required>

      <!-- Form Buttons -->
      <button type="submit">Save</button>
      <button type="button" @click="cancelForm">Cancel</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    
    return {
      isDivVisible: false,
      currentStatus : false,
      theatres: [],
      newTheatre: {
        name: null,
        capacity: null,
        address: null,
        code: null,
      },
      showForm: false,
    };
  },
  mounted() {
    this.loadTheatres();
  },
  methods: {
    seeStatus(){
      this.currentStatus = true
    },
    toggleDivVisibility() {
      // Toggle the visibility of the div
      this.isDivVisible = !this.isDivVisible;
    },
    async loadTheatres() {
      try {
        const response = await this.$http.get('theatres');
        this.theatres = response.data;
        console.log(this.theatres);
      } catch (error) {
        console.error('Error fetching theatres:', error);
      }
    },
    async saveTheatre() {
      try {
        const theaterData = {
          name: this.newTheatre.name,
          capacity: this.newTheatre.capacity,
          address: this.newTheatre.address,
          code: this.newTheatre.code,
        };
        console.log(theaterData)
        const response = await this.$http.post("theatre", theaterData);

        if (response.status === 201) {
          window.alert("Theatre added successfully!");
          this.$router.push("/theatremanagement"); 
          window.location.reload();
          this.cancelForm(); // Reset the form fields and hide the form
        } else {
          console.log(response.text);
        }
      } catch (error) {
        console.error("An error occurred:", error);
      }
    },
    editTheatre(theatreCode) {
      this.$router.push({ name: 'theatreedit', params: { theatreCode: theatreCode } });
    },
    async deleteTheatre(theatreCode) {
      const response = await this.$http.delete(`theatre/${theatreCode}`);
      window.alert("Theatre deleted successfully!");
      this.$router.push("/theatremanagement"); 
      window.location.reload();
    },
    cancelForm() {
      // Reset the form fields to their initial state
      this.newTheatre.name = null;
      this.newTheatre.capacity = null;
      this.newTheatre.address = null;
      this.newTheatre.code = null;

      // Hide the form
      this.showForm = false;
    },
  },
};

</script>

<style>
/* Style the table */
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

/* Style the form/modal */
form {
  display: flex;
  flex-direction: column;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

input[type="text"],
input[type="number"] {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 10px 15px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"] {
  background-color: #28a745;
}

button[type="submit"]:hover {
  background-color: #218838;
}

button[type="button"] {
  margin-right: 10px;
  background-color: #dc3545;
}

button[type="button"]:hover {
  background-color: #c82333;
}
</style>