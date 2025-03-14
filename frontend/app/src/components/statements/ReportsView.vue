<template>
  <div>
    <h2>Dochádzkové správy</h2>
    <v-row dense>
      <v-col cols="12" md="3">
        <v-select
            v-model="reportFilter.employee_id"
            :items="employees"
            item-value="employee_id"
            item-title="name"
            label="Zamestnanec"
            outlined
        ></v-select>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
            v-model="reportFilter.date_from"
            type="date"
            label="Dátum od"
            outlined
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
            v-model="reportFilter.date_to"
            type="date"
            label="Dátum do"
            outlined
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3" class="text-right">
        <v-btn color="primary" @click="generateAttendanceReport">
          Vygenerovať správu
        </v-btn>
      </v-col>
    </v-row>

    <div class="mt-4">
      <div v-if="reportResult">
        <h3>
          Dochádzková správa pre zamestnanca ID:
          {{ reportResult.employee_id }}
        </h3>
        <p>Rozsah dátumov: {{ reportResult.date_range }}</p>
        <p>
          <strong>Celkový odpracovaný čas:</strong>
          {{ formatHours(reportResult.total_hours_worked) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
const baseURL = process.env.VUE_APP_API_URL;

export default {
  name: 'ReportsView',
  props: {
    employees: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      reportFilter: {
        employee_id: null,
        date_from: '',
        date_to: '',
      },
      reportResult: null
    };
  },
  methods: {
    formatHours(hours) {
      if (!hours) return '0.00';
      return Number(hours).toFixed(2);
    },
    generateAttendanceReport() {
      const {employee_id, date_from, date_to} = this.reportFilter;
      if (!employee_id || !date_from || !date_to) {
        alert('Prosím, vyplňte všetky polia.');
        return;
      }

      const url = `${baseURL}/reports/attendance/?employee_id=${employee_id}&date_from=${date_from}&date_to=${date_to}`;
      fetch(url)
          .then(res => res.json())
          .then(data => {
            this.reportResult = data;
          })
          .catch(error => {
            console.error('Error:', error);
            alert('Nastala chyba pri generovaní správy.');
          });
    }
  }
};
</script> 