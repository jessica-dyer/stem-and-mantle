<template>
  <v-form @submit.prevent="submitForm">
    <v-container class="custom-container">
      <v-row justify="center">
        <v-col cols="12">
          <h1 class="form-title">ENTER CLIMB</h1>
        </v-col>
      </v-row>
      <v-autocomplete
        label="Gym"
        v-model="gym"
        :items="gyms"
        outlined
        dense
      ></v-autocomplete>

      <v-row justify="center">
        <v-col cols="12" class="mb-4">
          <datepicker
            color="primary"
            v-model="date"
            :typeable="true"
            placeholder="Climb date"
          ></datepicker>
        </v-col>
      </v-row>

      <v-autocomplete
        label="Grade given"
        v-model="grade_rated"
        :items="grades"
        outlined
        dense
      ></v-autocomplete>

      <v-autocomplete
        label="Grade feels like"
        v-model="grade_feels"
        :items="grades"
        outlined
        dense
      ></v-autocomplete>

      <v-autocomplete
        label="Style"
        v-model="style"
        :items="['Top Rope', 'Lead']"
        outlined
        dense
      ></v-autocomplete>

      <v-text-field
        label="Number of takes"
        v-model="number_of_takes"
        type="number"
        outlined
        dense
      ></v-text-field>

      <v-container fluid>
        <v-checkbox
            v-model="completed"
            label="Climb completed"
        ></v-checkbox>
      </v-container>
      
      <v-text-field
        label="Route Setter"
        v-model="setter"
        outlined
        dense
      ></v-text-field>

      <v-textarea label="Notes" v-model="notes" outlined dense></v-textarea>

      <v-row class="mt-4" justify="center">
        <v-col cols="auto">
          <v-btn @click="submitForm" color="primary">
            Submit
          </v-btn>
        </v-col>
        <v-col cols="auto">
          <v-btn @click="clearForm" color="secondary">
            Clear Form
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>
  
  <script>
  import Datepicker from 'vuejs3-datepicker';
  import axios from 'axios';

  export default {
    components: {Datepicker},
    data() {
      return {
        gym: "Vertical World: Seattle",
        gyms: ["Vertical World: Seattle", "Vertical World: North"],
        date: new Date(),
        completed: true,
        grade_rated: "5.9",
        grade_feels: null,
        grades: ["5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9", "5.10"],
        style: "Lead",
        number_of_takes: 0,
        setter: "jd",
        notes: "",
        };
    },
    methods: {
      submitForm() {
      const year = this.date.getFullYear();
      const month = this.date.getMonth() + 1;
      const day = this.date.getDate();

      // Create a formatted date string in 'YYYY-MM-DD' format
      const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
      const formData = {
        user_id: 1, 
        training_session_id: 1,
        gym: this.gym,
        date: formattedDate,
        grade_rated: this.grade_rated,
        grade_feels: this.grade_feels,
        style: this.style,
        number_of_takes: this.number_of_takes,
        completed: this.completed,
        setter: this.setter,
        notes: this.notes,
      };
      axios
      .post('http://localhost:8000/climbs/', formData)
      .then(response => {
        console.log('API response:', response.data);
        // You can also perform any actions after successful submission
        // For example, show a success message or navigate to another page
      })
      .catch(error => {
        // Handle any errors that occurred during the API request
        console.error('API error:', error);
        // You can show an error message to the user or take appropriate actions
      });
    },
      clearForm() {
      // Set the form data properties to their initial values or clear them
      this.gym = '';
      this.selectedCountry = '';
      this.givenGrade = '';
      this.gradeFeelsLike = '';
      this.style = '';
      this.numberValue = '';
      this.completed = null; // or false, depending on your initial value
      this.setter = '';
      this.notes = '';
    },
    },
  };
  </script>
  
  <style>
/* Custom styles for the form */
.custom-container {
  max-width: 600px; /* Limit the width of the form */
  margin: auto; /* Center the form horizontally */
  padding: 20px; /* Add padding around the form */
  background-color: #f7f7f7; /* Set a background color */
  border-radius: 10px; /* Add rounded corners */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Add a subtle box shadow */
}

/* Style the submit button */
.custom-container v-btn {
  margin-top: 20px; /* Add space between the form and the button */
}

/* Style the input fields */
.custom-container v-text-field,
.custom-container v-autocomplete,
.custom-container v-select,
.custom-container v-date-picker,
.custom-container v-radio-group,
.custom-container v-textarea {
  margin-bottom: 10px; /* Add space between the fields */
}

/* Style the form title */
.form-title {
  text-align: center;
  margin-bottom: 20px;
}

/* Adjust spacing for the radio group */
.custom-container v-radio {
  margin-right: 20px;
}

/* Center the buttons in the row */
.custom-container .mt-4 {
  justify-content: center;
}
</style>