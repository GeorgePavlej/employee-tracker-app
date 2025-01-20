<template>
  <div>
    <v-toolbar color="primary" dark>
      <v-toolbar-title>Employee Manager</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Menu Buttons -->
      <v-btn
          text
          :class="{'font-weight-bold underline': currentSection === 'clockInOut'}"
          @click="showSection('clockInOut')"
      >
        Clock In/Out
      </v-btn>

      <v-btn
          text
          :class="{'font-weight-bold underline': currentSection === 'logs'}"
          @click="showSection('logs')"
      >
        Logs
      </v-btn>

      <v-btn
          text
          :class="{'font-weight-bold underline': currentSection === 'shifts'}"
          @click="showSection('shifts')"
      >
        Shifts
      </v-btn>

      <v-btn
          text
          :class="{'font-weight-bold underline': currentSection === 'reports'}"
          @click="showSection('reports')"
      >
        Reports
      </v-btn>

      <v-btn
          text
          :class="{'font-weight-bold underline': currentSection === 'leaveManagement'}"
          @click="showSection('leaveManagement')"
      >
        Leave Management
      </v-btn>

      <v-btn
          text
          :class="{'font-weight-bold underline': currentSection === 'employeeManagement'}"
          @click="showSection('employeeManagement')"
      >
        Employee Management
      </v-btn>
    </v-toolbar>

    <!-- Main Content -->
    <v-container fluid class="mt-4">
      <!-- CLOCK IN/OUT SECTION -->
      <div v-if="currentSection === 'clockInOut'">
        <h2>Clock In/Out</h2>
        <v-select
            v-model="selectedEmployeeClock"
            :items="employees"
            item-title="name"
            item-value="employee_id"
            label="Select Employee"
            outlined
        ></v-select>

        <div class="mt-4">
          <v-btn
              color="primary"
              class="mr-2"
              @click="clockIn"
              :disabled="!selectedEmployeeClock"
          >
            Clock In
          </v-btn>
          <v-btn
              color="secondary"
              class="mr-2"
              @click="clockOut"
              :disabled="!selectedEmployeeClock"
          >
            Clock Out
          </v-btn>
          <v-btn
              color="warning"
              class="mr-2"
              @click="startLunch"
              :disabled="!selectedEmployeeClock"
          >
            Start Lunch
          </v-btn>
          <v-btn
              color="success"
              @click="endLunch"
              :disabled="!selectedEmployeeClock"
          >
            End Lunch
          </v-btn>
        </div>
      </div>

      <!-- LOGS SECTION -->
      <div v-if="currentSection === 'logs'">
        <h2>View Logs</h2>
        <v-row dense>
          <v-col cols="12" md="3">
            <v-text-field
                v-model="logsFilter.name"
                label="Employee Name (contains)"
                outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
                v-model="logsFilter.dateFrom"
                type="date"
                label="Date From"
                outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
                v-model="logsFilter.dateTo"
                type="date"
                label="Date To"
                outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3" class="text-right">
            <v-btn color="primary" @click="viewLogs">Filter Logs</v-btn>
          </v-col>
        </v-row>

        <v-data-table :items="logs" class="mt-4" dense>
          <template v-slot:headers>
            <tr>
              <th class="text-left">Employee Name</th>
              <th class="text-left">Date</th>
              <th class="text-left">Clock In</th>
              <th class="text-left">Clock Out</th>
              <th class="text-left">Lunch Start</th>
              <th class="text-left">Lunch End</th>
            </tr>
          </template>
          <template v-slot:body="{ items }">
            <tr v-if="items.length === 0">
              <td colspan="6" class="text-center">No logs found for the given filters.</td>
            </tr>
            <tr v-for="(log, index) in items" :key="index">
              <td>{{ log.employee_name }}</td>
              <td>{{ log.date }}</td>
              <td>{{ log.clock_in_time || 'N/A' }}</td>
              <td>{{ log.clock_out_time || 'N/A' }}</td>
              <td>{{ log.lunch_start_time || 'N/A' }}</td>
              <td>{{ log.lunch_end_time || 'N/A' }}</td>
            </tr>
          </template>
        </v-data-table>
      </div>

      <!-- SHIFTS SECTION -->
      <div v-if="currentSection === 'shifts'">
        <h2>Shift Scheduling</h2>
        <v-form ref="shiftForm">
          <v-row dense>
            <v-col cols="12" md="3">
              <v-select
                  v-model="shiftFormData.employee_id"
                  :items="employees"
                  item-value="employee_id"
                  item-title="name"
                  label="Employee"
                  outlined
              ></v-select>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field
                  v-model="shiftFormData.date"
                  type="date"
                  label="Date"
                  outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field
                  v-model="shiftFormData.start_time"
                  type="time"
                  label="Start Time"
                  outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field
                  v-model="shiftFormData.end_time"
                  type="time"
                  label="End Time"
                  outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="text-right">
              <v-btn color="primary" @click="createShift">Create Shift</v-btn>
            </v-col>
          </v-row>
        </v-form>

        <hr class="my-4"/>

        <h3>View Scheduled Shifts</h3>
        <v-row dense>
          <v-col cols="12" md="3">
            <v-select
                v-model="shiftFilter.employee_id"
                :items="employees"
                item-value="employee_id"
                item-title="name"
                label="Employee"
                outlined
            ></v-select>
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
                v-model="shiftFilter.date_from"
                type="date"
                label="Date From"
                outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
                v-model="shiftFilter.date_to"
                type="date"
                label="Date To"
                outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3" class="text-right">
            <v-btn color="primary" @click="loadShifts">Filter Shifts</v-btn>
          </v-col>
        </v-row>

        <v-data-table :items="shifts" class="mt-3" dense>
          <template v-slot:headers>
            <tr>
              <th>Employee Name</th>
              <th>Date</th>
              <th>Start</th>
              <th>End</th>
            </tr>
          </template>
          <template v-slot:body="{ items }">
            <tr v-if="items.length === 0">
              <td colspan="4" class="text-center">No shifts found for the given filters.</td>
            </tr>
            <tr v-for="(shift, index) in items" :key="index">
              <td>{{ shift.employee_name }}</td>
              <td>{{ shift.date }}</td>
              <td>{{ shift.start_time }}</td>
              <td>{{ shift.end_time }}</td>
            </tr>
          </template>
        </v-data-table>
      </div>

      <!-- REPORTS SECTION -->
      <div v-if="currentSection === 'reports'">
        <h2>Attendance Reports</h2>
        <v-row dense>
          <v-col cols="12" md="3">
            <v-select
              v-model="reportFilter.employee_id"
              :items="employees"
              item-value="employee_id"
              item-title="name"
              label="Employee"
              outlined
            ></v-select>
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="reportFilter.date_from"
              type="date"
              label="Date From"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="reportFilter.date_to"
              type="date"
              label="Date To"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3" class="text-right">
            <v-btn color="primary" @click="generateAttendanceReport"
            >Generate Report
            </v-btn
            >
          </v-col>
        </v-row>

        <div class="mt-4">
          <div v-if="reportResult">
            <h3>Attendance Report for Employee ID: {{ reportResult.employee_id }}</h3>
            <p>Date Range: {{ reportResult.date_range }}</p>
            <p>
              <strong>Total Hours Worked:</strong>
              {{ formatHours(reportResult.total_hours_worked) }}
            </p>
          </div>
        </div>
      </div>

      <!-- LEAVE MANAGEMENT SECTION -->
      <div v-if="currentSection === 'leaveManagement'">
        <h2>Leave Management</h2>
        <h4>Submit a Leave Request</h4>
        <v-form ref="leaveForm">
          <v-row dense>
            <v-col cols="12" md="3">
              <v-select
                  v-model="leaveRequest.employee_id"
                  :items="employees"
                  item-value="employee_id"
                  item-title="name"
                  label="Employee"
                  outlined
              ></v-select>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field
                  v-model="leaveRequest.start_date"
                  type="date"
                  label="Start Date"
                  outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field
                  v-model="leaveRequest.end_date"
                  type="date"
                  label="End Date"
                  outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                  v-model="leaveRequest.reason"
                  label="Reason (optional)"
                  outlined
                  textarea
                  rows="2"
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="text-right">
              <v-btn color="primary" @click="submitLeaveRequest"
              >Submit Leave Request
              </v-btn
              >
            </v-col>
          </v-row>
        </v-form>

        <hr class="my-4"/>

        <h3>Leave Requests</h3>
        <v-data-table :items="leaveRequests" dense>
          <template v-slot:headers>
            <tr>
              <th>Employee Name</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Reason</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </template>
          <template v-slot:body="{ items }">
            <tr v-if="items.length === 0">
              <td colspan="6" class="text-center">No leave requests found.</td>
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
                    Approve
                  </v-btn>
                  <v-btn
                      color="error"
                      small
                      @click="updateLeaveRequestStatus(request.leave_id, 'Rejected')"
                  >
                    Reject
                  </v-btn>
                </div>
              </td>
            </tr>
          </template>
        </v-data-table>
      </div>

      <!-- ========================================== -->
      <!--         EMPLOYEE MANAGEMENT SECTION       -->
      <!-- ========================================== -->
      <div v-if="currentSection === 'employeeManagement'">
        <h2>Employee Management</h2>

        <v-form ref="employeeForm">
          <v-row dense>
            <v-col cols="12" md="4">
              <v-text-field
                  v-model="employeeFormData.name"
                  label="Employee Name"
                  outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4" class="text-right">
              <v-btn
                  color="primary"
                  v-if="!editMode"
                  @click="createEmployee"
              >
                Create Employee
              </v-btn>

              <v-btn
                  color="success"
                  v-if="editMode"
                  @click="updateEmployee"
              >
                Update Employee
              </v-btn>

              <v-btn
                  color="secondary"
                  v-if="editMode"
                  @click="cancelEdit"
              >
                Cancel
              </v-btn>
            </v-col>
          </v-row>
        </v-form>

        <hr class="my-4"/>

        <v-data-table :items="employees" dense>
          <template v-slot:headers>
            <tr>
              <th>Employee ID</th>
              <th>Name</th>
              <th class="text-right">Actions</th>
            </tr>
          </template>
          <template v-slot:body="{ items }">
            <tr v-if="items.length === 0">
              <td colspan="3" class="text-center">
                No employees found.
              </td>
            </tr>
            <tr v-for="(emp, index) in items" :key="index">
              <td>{{ emp.employee_id }}</td>
              <td>{{ emp.name }}</td>
              <td class="text-right">
                <v-btn
                    small
                    color="warning"
                    @click="editEmployee(emp)"
                >
                  Edit
                </v-btn>
                <v-btn
                    small
                    color="error"
                    @click="deleteEmployee(emp.employee_id)"
                >
                  Delete
                </v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </div>
    </v-container>
  </div>
</template>

<script>

const baseURL = process.env.VUE_APP_API_URL;
export default {
  name: 'Statements',
  data() {
    return {
      currentSection: 'clockInOut',

      employees: [],
      selectedEmployeeClock: null,

      logsFilter: {
        name: '',
        dateFrom: '',
        dateTo: ''
      },
      logs: [],

      shiftFormData: {
        employee_id: null,
        date: '',
        start_time: '',
        end_time: ''
      },

      shiftFilter: {
        employee_id: null,
        date_from: '',
        date_to: ''
      },
      shifts: [],

      reportFilter: {
        employee_id: null,
        date_from: '',
        date_to: ''
      },
      reportResult: null,

      leaveRequest: {
        employee_id: null,
        start_date: '',
        end_date: '',
        reason: '',
      },
      leaveRequests: [],

      employeeFormData: {
        employee_id: null,
        name: '',
      },
      editMode: false,
    };
  },

  created() {
    this.loadEmployees();
  },

  methods: {
    showSection(sectionId) {
      this.currentSection = sectionId;

      if (sectionId === 'shifts') {
        this.loadShifts();
      } else if (sectionId === 'logs') {
        this.viewLogs();
      } else if (sectionId === 'leaveManagement') {
        this.loadLeaveRequests();
      } else if (sectionId === 'reports') {
        this.reportResult = null;
      } else if (sectionId === 'employeeManagement') {
        this.loadEmployees();
        this.cancelEdit();
      }
    },

    formatHours(hours) {
      if (!hours) return '0.00';
      return Number(hours).toFixed(2);
    },

    // ---- EMPLOYEES ----
    loadEmployees() {
      fetch(`${baseURL}/employees/`)
          .then((res) => res.json())
          .then((data) => {
            console.log('Employees fetched:', data);
            this.employees = data;
          })
          .catch((error) => console.error('Error fetching employees:', error));
    },

    // ---- CLOCK IN/OUT ----
    clockIn() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/clock_in/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then((res) => res.json())
          .then((data) => {
            alert(data.message || data.detail);
          })
    },
    clockOut() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/clock_out/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then((res) => res.json())
          .then((data) => {
            alert(data.message || data.detail);
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while clocking out.');
          });
    },
    startLunch() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/start_lunch/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then((res) => res.json())
          .then((data) => {
            alert(data.message || data.detail);
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while starting lunch.');
          });
    },
    endLunch() {
      if (!this.selectedEmployeeClock) return;
      fetch(`${baseURL}/end_lunch/?employee_id=${this.selectedEmployeeClock}`, {
        method: 'POST',
      })
          .then((res) => res.json())
          .then((data) => {
            alert(data.message || data.detail);
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while ending lunch.');
          });
    },

    // ---- LOGS ----
    viewLogs() {
      const nameFilter = this.logsFilter.name;
      const dateFrom = this.logsFilter.dateFrom;
      const dateTo = this.logsFilter.dateTo;

      let url = `${baseURL}/logs/?`;
      const params = [];
      if (nameFilter) {
        params.push(`employee_name=${encodeURIComponent(nameFilter)}`);
      }
      if (dateFrom) {
        params.push(`date_from=${dateFrom}`);
      }
      if (dateTo) {
        params.push(`date_to=${dateTo}`);
      }
      url += params.join('&');

      fetch(url)
          .then((res) => res.json())
          .then((data) => {
            this.logs = data;
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while fetching logs.');
          });
    },

    // ---- SHIFTS ----
    createShift() {
      const {employee_id, date, start_time, end_time} = this.shiftFormData;
      if (!employee_id || !date || !start_time || !end_time) {
        alert('Please fill in all fields.');
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
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error creating shift.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert('Shift created successfully.');
            this.shiftFormData.employee_id = null;
            this.shiftFormData.date = '';
            this.shiftFormData.start_time = '';
            this.shiftFormData.end_time = '';
            this.loadShifts();
          })
          .catch((error) => {
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
          .then((res) => res.json())
          .then((data) => {
            this.shifts = data;
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while fetching shifts.');
          });
    },

    // ---- REPORTS ----
    generateAttendanceReport() {
      const {employee_id, date_from, date_to} = this.reportFilter;
      if (!employee_id || !date_from || !date_to) {
        alert('Please fill in all fields.');
        return;
      }

      const url = `${baseURL}/reports/attendance/?employee_id=${employee_id}&date_from=${date_from}&date_to=${date_to}`;
      fetch(url)
          .then((res) => res.json())
          .then((data) => {
            this.reportResult = data;
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while generating the report.');
          });
    },

    // ---- LEAVE MANAGEMENT ----
    submitLeaveRequest() {
      const {employee_id, start_date, end_date, reason} = this.leaveRequest;
      if (!employee_id || !start_date || !end_date) {
        alert('Please fill in all required fields.');
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
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error submitting leave request.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert('Leave request submitted successfully.');
            this.leaveRequest.employee_id = null;
            this.leaveRequest.start_date = '';
            this.leaveRequest.end_date = '';
            this.leaveRequest.reason = '';
            this.loadLeaveRequests();
          })
          .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
          });
    },
    loadLeaveRequests() {
      fetch(`${baseURL}/leave_requests/`)
          .then((res) => res.json())
          .then((data) => {
            this.leaveRequests = data;
          })
          .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while fetching leave requests.');
          });
    },
    updateLeaveRequestStatus(leaveId, status) {
      fetch(`${baseURL}/leave_requests/${leaveId}/?status=${status}`, {
        method: 'PUT',
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error updating leave request.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert(`Leave request ${status.toLowerCase()} successfully.`);
            this.loadLeaveRequests();
          })
          .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
          });
    },

    // ======================================
    //          EMPLOYEE MANAGEMENT
    // ======================================

    createEmployee() {
      if (!this.employeeFormData.name) {
        alert('Please enter a name.');
        return;
      }
      fetch(`${baseURL}/employees/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: this.employeeFormData.name}),
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error creating employee.');
              });
            }
            return res.json();
          })
          .then((newEmployee) => {
            alert('Employee created successfully.');
            this.employeeFormData.name = '';
            this.loadEmployees();
          })
          .catch((error) => {
            console.error(error);
            alert(error.message);
          });
    },

    deleteEmployee(employeeId) {
      if (!confirm('Are you sure you want to delete this employee?')) return;
      fetch(`${baseURL}/employees/${employeeId}/`, {
        method: 'DELETE',
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error deleting employee.');
              });
            }
            return res.json();
          })
          .then(() => {
            alert('Employee deleted successfully.');
            this.loadEmployees();
          })
          .catch((error) => {
            console.error(error);
            alert(error.message);
          });
    },

    editEmployee(emp) {
      this.editMode = true;
      this.employeeFormData.employee_id = emp.employee_id;
      this.employeeFormData.name = emp.name;
    },

    // UPDATE
    updateEmployee() {
      const {employee_id, name} = this.employeeFormData;
      if (!employee_id || !name) {
        alert('Invalid data.');
        return;
      }
      fetch(`${baseURL}/employees/${employee_id}/`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name}),
      })
          .then((res) => {
            if (!res.ok) {
              return res.json().then((data) => {
                throw new Error(data.detail || 'Error updating employee.');
              });
            }
            return res.json();
          })
          .then((updatedEmployee) => {
            alert('Employee updated successfully.');
            this.cancelEdit();
            this.loadEmployees();
          })
          .catch((error) => {
            console.error(error);
            alert(error.message);
          });
    },

    cancelEdit() {
      this.editMode = false;
      this.employeeFormData.employee_id = null;
      this.employeeFormData.name = '';
    },
  },
};
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/vuetify@3.3.7/dist/vuetify.min.css');
@import url('https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900');
@import url('https://cdn.jsdelivr.net/npm/@mdi/font@6.9.96/css/materialdesignicons.min.css');

.underline {
  text-decoration: underline;
}

.font-weight-bold {
  font-weight: 600 !important;
}

.mb-3 {
  margin-bottom: 16px;
}

.mt-4 {
  margin-top: 24px;
}
</style>
