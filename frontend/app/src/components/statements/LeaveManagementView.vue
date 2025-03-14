<template>
  <div>
    <h2>Správa dovoleniek</h2>
    <h4>Odoslať žiadosť o dovolenku</h4>
    <v-form ref="leaveForm">
      <v-row dense>
        <v-col cols="12" md="3">
          <v-select
              v-model="leaveRequest.employee_id"
              :items="employees"
              item-value="employee_id"
              item-title="name"
              label="Zamestnanec"
              outlined
          ></v-select>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
              v-model="leaveRequest.start_date"
              type="date"
              label="Dátum začiatku"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
              v-model="leaveRequest.end_date"
              type="date"
              label="Dátum ukončenia"
              outlined
          ></v-text-field>
        </v-col>
        <v-col cols="12">
          <v-text-field
              v-model="leaveRequest.reason"
              label="Dôvod (nepovinné)"
              outlined
              textarea
              rows="2"
          ></v-text-field>
        </v-col>
        <v-col cols="12" class="text-right">
          <v-btn color="primary" @click="submitLeaveRequest">
            Odoslať žiadosť o dovolenku
          </v-btn>
        </v-col>
      </v-row>
    </v-form>

    <hr class="my-4"/>

    <h3>Žiadosti o dovolenku</h3>
    <v-data-table :items="leaveRequests" dense>
      <template v-slot:headers>
        <tr>
          <th>Meno zamestnanca</th>
          <th>Dátum začiatku</th>
          <th>Dátum ukončenia</th>
          <th>Dôvod</th>
          <th>Stav</th>
          <th>Akcie</th>
        </tr>
      </template>
      <template v-slot:body="{ items }">
        <tr v-if="items.length === 0">
          <td colspan="6" class="text-center">
            Žiadne žiadosti o dovolenku neboli nájdené.
          </td>
        </tr>
        <tr v-for="(request, index) in items" :key="index">
          <td>{{ request.employee_name }}</td>
          <td>{{ request.start_date }}</td>
          <td>{{ request.end_date }}</td>
          <td>{{ request.reason || '' }}</td>
          <td>{{ request.status }}</td>
          <td>
            <div v-if="request.status === 'Pending'">
              <v-btn
                  color="success"
                  small
                  @click="updateLeaveRequestStatus(request.leave_id, 'Approved')"
              >
                Schváliť
              </v-btn>
              <v-btn
                  color="error"
                  small
                  @click="updateLeaveRequestStatus(request.leave_id, 'Rejected')"
              >
                Zamietnuť
              </v-btn>
            </div>
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
const baseURL = process.env.VUE_APP_API_URL;

export default {
  name: 'LeaveManagementView',
  props: {
    employees: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      leaveRequest: {
        employee_id: null,
        start_date: '',
        end_date: '',
        reason: '',
      },
      leaveRequests: []
    };
  },
  created() {
    this.loadLeaveRequests();
  },
  methods: {
    submitLeaveRequest() {
      const {employee_id, start_date, end_date, reason} = this.leaveRequest;
      if (!employee_id || !start_date || !end_date) {
        alert('Prosím, vyplňte všetky povinné polia.');
        return;
      }

      fetch(`${baseURL}/leave_requests/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          employee_id: parseInt(employee_id),
          start_date,
          end_date,
          reason,
        }),
      })
          .then(res => {
            if (!res.ok) {
              return res.json().then(data => {
                throw new Error(data.detail || 'Chyba pri odosielaní žiadosti o dovolenku.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert('Žiadosť o dovolenku bola úspešne odoslaná.');
            this.leaveRequest.employee_id = null;
            this.leaveRequest.start_date = '';
            this.leaveRequest.end_date = '';
            this.leaveRequest.reason = '';
            this.loadLeaveRequests();
          })
          .catch(error => {
            console.error('Error:', error);
            alert(error.message);
          });
    },
    loadLeaveRequests() {
      fetch(`${baseURL}/leave_requests/`)
          .then(async res => {
            if (!res.ok) {
              let err = 'Chyba pri načítaní žiadostí o dovolenku.';
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
            this.leaveRequests = Array.isArray(data) ? data : [];
          })
          .catch(error => {
            console.error('Error:', error);
            alert(error.message);
          });
    },
    updateLeaveRequestStatus(leaveId, status) {
      fetch(`${baseURL}/leave_requests/${leaveId}/?status=${status}`, {
        method: 'PUT',
      })
          .then(res => {
            if (!res.ok) {
              return res.json().then(data => {
                throw new Error(data.detail || 'Chyba pri aktualizácii žiadosti o dovolenku.');
              });
            }
            return res.json();
          })
          .then(() => {
            const statusText = status === 'Approved' ? 'schválená' : 'zamietnutá';
            alert(`Žiadosť o dovolenku bola úspešne ${statusText}.`);
            this.loadLeaveRequests();
          })
          .catch(error => {
            console.error('Error:', error);
            alert(error.message);
          });
    }
  }
};
</script> 