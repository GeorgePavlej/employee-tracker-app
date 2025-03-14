<template>
  <div>
    <h2>Plánovanie zmien</h2>
    <v-form ref="shiftForm">
      <v-row dense>
        <v-col cols="12" md="3">
          <v-select
              v-model="shiftFormData.employee_id"
              :items="employees"
              item-value="employee_id"
              item-title="name"
              label="Zamestnanec"
              outlined
          ></v-select>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
              v-model="shiftFormData.date"
              type="date"
              label="Dátum"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
              v-model="shiftFormData.start_time"
              type="time"
              label="Čas začiatku"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
              v-model="shiftFormData.end_time"
              type="time"
              label="Čas ukončenia"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" class="text-right">
          <v-btn color="primary" @click="createShift">
            Vytvoriť zmenu
          </v-btn>
        </v-col>
      </v-row>
    </v-form>

    <hr class="my-4"/>

    <h3>Zobraziť plánované zmeny</h3>
    <v-row dense>
      <v-col cols="12" md="3">
        <v-select
            v-model="shiftFilter.employee_id"
            :items="employees"
            item-value="employee_id"
            item-title="name"
            label="Zamestnanec"
            outlined
        ></v-select>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
            v-model="shiftFilter.date_from"
            type="date"
            label="Dátum od"
            outlined
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
            v-model="shiftFilter.date_to"
            type="date"
            label="Dátum do"
            outlined
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3" class="text-right">
        <v-btn color="primary" @click="loadShifts">
          Filtrovať zmeny
        </v-btn>
      </v-col>
    </v-row>

    <hr class="my-4"/>

    <h3>Kalendár zmien</h3>

    <v-calendar
        type="month"
        :events="calendarEvents"
        :event-order="orderEvents"
        height="600"
    >
      <template #event="{ event }">
        <div
            class="custom-event d-flex align-center"
            :style="{ backgroundColor: event.color }"
        >
          <strong>{{ formatTime(event.start) }} - {{ formatTime(event.end) }}</strong>
          <span class="ml-2">{{ event.title }}</span>
        </div>
      </template>
    </v-calendar>
  </div>
</template>

<script>
const baseURL = process.env.VUE_APP_API_URL;

export default {
  name: 'ShiftsView',
  props: {
    employees: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      shiftFormData: {
        employee_id: null,
        date: '',
        start_time: '',
        end_time: '',
      },
      shiftFilter: {
        employee_id: null,
        date_from: '',
        date_to: '',
      },
      shifts: []
    };
  },
  computed: {
    calendarEvents() {
      const colorChoices = ['blue', 'green', 'red', 'orange', 'purple'];
      return this.shifts.map(shift => {
        const startStr = `${shift.date}T${shift.start_time}`;
        const endStr = `${shift.date}T${shift.end_time}`;

        const startDate = new Date(startStr);
        const endDate = new Date(endStr);

        const randomColor = colorChoices[Math.floor(Math.random() * colorChoices.length)];

        return {
          title: `${shift.employee_name}`,
          start: startDate,
          end: endDate,
          color: randomColor,
        };
      });
    }
  },
  created() {
    this.loadShifts();
  },
  methods: {
    orderEvents(a, b) {
      return a.start - b.start
    },
    formatTime(dateObj) {
      if (!(dateObj instanceof Date)) return '';
      return new Intl.DateTimeFormat('sk-SK', {
        hour: 'numeric',
        minute: 'numeric',
      }).format(dateObj);
    },
    createShift() {
      const {employee_id, date, start_time, end_time} = this.shiftFormData;
      if (!employee_id || !date || !start_time || !end_time) {
        alert('Prosím, vyplňte všetky polia.');
        return;
      }

      fetch(`${baseURL}/shifts/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          employee_id: parseInt(employee_id),
          date,
          start_time,
          end_time,
        }),
      })
          .then(res => {
            if (!res.ok) {
              return res.json().then(data => {
                throw new Error(data.detail || 'Error creating shift.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert('Zmena bola úspešne vytvorená.');
            this.shiftFormData.employee_id = null;
            this.shiftFormData.date = '';
            this.shiftFormData.start_time = '';
            this.shiftFormData.end_time = '';
            this.loadShifts();
          })
          .catch(error => {
            console.error('Error:', error);
            alert(error.message);
          });
    },
    loadShifts() {
      const {employee_id, date_from, date_to} = this.shiftFilter;
      let url = `${baseURL}/shifts/?`;
      const params = [];

      if (employee_id) {
        params.push(`employee_id=${employee_id}`);
      }
      if (date_from) {
        params.push(`date_from=${date_from}`);
      }
      if (date_to) {
        params.push(`date_to=${date_to}`);
      }
      url += params.join('&');

      fetch(url)
          .then(async res => {
            if (!res.ok) {
              let err = 'Chyba pri načítaní zmien.';
              try {
                const data = await res.json();
                err = data.detail || err;
              } catch {
              }
              throw new Error(err);
            }
            return res.json();
          })
          .then(data => {
            this.shifts = Array.isArray(data) ? data : [];
          })
          .catch(error => {
            console.error('Error:', error);
            alert(error.message);
          });
    }
  }
};
</script>

<style scoped>
.custom-event {
  padding: 2px 4px;
  margin-bottom: 2px;
  border-radius: 4px;
  color: #fff;
  font-size: 0.75rem;
}
</style> 