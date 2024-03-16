<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Contacts</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="toggleAddContactModal">
          Add Contact
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">First Name</th>
              <th scope="col">Last Name</th>
              <th scope="col">Email</th>
              <th scope="col">Phone Number</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(contact, index) in contacts" :key="index">
              <td>{{ contact.first_name }}</td>
              <td>{{ contact.last_name }}</td>
              <td>{{ contact.email }}</td>
              <td>{{ contact.phone_number }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                      type="button"
                      class="btn btn-warning btn-sm"
                      @click="toggleEditContactModal(contact)">
                    Update
                  </button>
                  <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="handleDeleteContact(contact)">
                    Delete
                  </button>
                  <button
                      type="button"
                      class="btn btn-primary btn-sm"
                      @click="toggleHistoryModal(contact)">
                    History
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- add new contact modal -->
    <div
      ref="addContactModal"
      class="modal fade"
      :class="{ show: activeAddContactModal, 'd-block': activeAddContactModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a new contact</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddContactModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div v-if="errorMessage" class="alert alert-danger" role="alert">
              {{ errorMessage }}
            </div>
            <form>
              <div class="mb-3">
                <label for="addContactFirstName" class="form-label">First Name:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addContactFirstName"
                  v-model="addContactForm.first_name"
                  placeholder="Enter first name">
              </div>
              <div class="mb-3">
                <label for="addContactLastName" class="form-label">Last Name:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addContactLastName"
                  v-model="addContactForm.last_name"
                  placeholder="Enter last name">
              </div>
              <div class="mb-3">
                <label for="addContactEmail" class="form-label">Email:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addContactEmail"
                  v-model="addContactForm.email"
                  placeholder="Enter email">
              </div>
              <div class="mb-3">
                <label for="addContactPhoneNumber" class="form-label">Phone Number:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addContactPhoneNumber"
                  v-model="addContactForm.phone_number"
                  placeholder="Enter phone number">
              </div>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleAddSubmit">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleAddReset">
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddContactModal" class="modal-backdrop fade show"></div>
  
  <!-- edit contact modal -->
    <div
  ref="editContactModal"
  class="modal fade"
  :class="{ show: activeEditContactModal, 'd-block': activeEditContactModal }"
  tabindex="-1"
  role="dialog">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Update</h5>
        <button
          type="button"
          class="close"
          data-dismiss="modal"
          aria-label="Close"
          @click="toggleEditContactModal">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>
        <form>
          <div class="mb-3">
            <label for="editContactFirstName" class="form-label">First Name:</label>
            <input
              type="text"
              class="form-control"
              id="editContactFirstName"
              v-model="editContactForm.first_name"
              placeholder="Enter first name">
          </div>
          <div class="mb-3">
            <label for="editContactLastName" class="form-label">Last Name:</label>
            <input
              type="text"
              class="form-control"
              id="editContactLastName"
              v-model="editContactForm.last_name"
              placeholder="Enter last name">
          </div>
          <div class="mb-3">
            <label for="editContactEmail" class="form-label">Email:</label>
            <input
              type="text"
              class="form-control"
              id="editContactEmail"
              v-model="editContactForm.email"
              placeholder="Enter email">
          </div>
          <div class="mb-3">
            <label for="editContactPhoneNumber" class="form-label">Phone Number:</label>
            <input
              type="text"
              class="form-control"
              id="editContactPhoneNumber"
              v-model="editContactForm.phone_number"
              placeholder="Enter phone number">
          </div>
          <div class="btn-group" role="group">
            <button
              type="button"
              class="btn btn-primary btn-sm"
              @click="handleEditSubmit">
              Submit
            </button>
            <button
              type="button"
              class="btn btn-danger btn-sm"
              @click="handleEditCancel">
              Cancel
            </button>
           </div>
         </form>
        </div>
      </div>
    </div>
  </div>
  <div v-if="activeEditContactModal" class="modal-backdrop fade show"></div>

    <!-- history modal -->
    <div
      ref="HistoryModal"
      class="modal fade"
      :class="{ show: activeHistoryModal, 'd-block': activeHistoryModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">History (last 10 changes)</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleHistoryModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <table class="table">
              <thead>
                <tr>
                  <th>Action</th>
                  <th>Created At</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="entry in changelog" :key="entry.id">
                  <td>{{ entry.action }}</td>
                  <td>{{ entry.created_at }}</td>
                  <td>{{ entry.description }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeHistoryModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      activeAddContactModal: false,
      addContactForm: {
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
      },
      activeEditContactModal: false,
      editContactForm: {
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
      },
      activeHistoryModal: false,
      changelog: [],

      contacts: [],
      message: '',
      showMessage: false,
      errorMessage: '',
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    addContact(payload) {
      const path = 'http://localhost:5001/contacts';
      axios.post(path, payload)
        .then(() => {
          this.getContacts();
          this.message = 'Contact added!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.getContacts();
        });
    },
    getContacts() {
      const path = 'http://localhost:5001/contacts';
      axios.get(path)
        .then((res) => {
          this.contacts = res.data.contacts;
        })
        .catch((error) => {

          console.error(error);
        });
    },
    checkDuplicateEmail(email) {
      // debugger;
      if (this.editContactForm.id) {
          // If the new email is the same as the current email of the contact being edited
          if (this.initialEmail !== email) {
              const filteredContacts = this.contacts.filter(contact => contact.id !== this.editContactForm.id);
              return filteredContacts.some(contact => contact.email === email);
          }
      } else {
        return this.contacts.some(contact => contact.email === email);
      }
      return false
    },
    handleAddReset() {
      this.errorMessage = '';
      this.initForm();
    },
    handleAddSubmit() {
      if (this.checkDuplicateEmail(this.addContactForm.email)) {
        this.errorMessage = 'Email already exists!';
        return;
      }
      this.errorMessage = '';
      this.toggleAddContactModal();
      const payload = {
        first_name: this.addContactForm.first_name,
        last_name: this.addContactForm.last_name,
        email: this.addContactForm.email,
        phone_number: this.addContactForm.phone_number,
      };
      this.addContact(payload);
      this.initForm();
    },
    handleEditSubmit() {
      if (this.checkDuplicateEmail(this.editContactForm.email)) {
        this.errorMessage = 'Email already exists!';
        return;
      }

      this.toggleEditContactModal(null);
      const payload = {
          first_name: this.editContactForm.first_name,
          last_name: this.editContactForm.last_name,
          email: this.editContactForm.email,
          phone_number: this.editContactForm.phone_number,
      };
      this.updateContact(payload, this.editContactForm.id);
      this.initForm();
    },
    updateContact(payload, contactID) {
      const path = `http://localhost:5001/contacts/${contactID}`;
      axios.put(path, payload)
          .then(() => {
              this.getContacts();
              this.message = 'Contact updated!';
              this.showMessage = true;
          })
          .catch((error) => {
              console.error(error);
              this.getContacts();
          });
    },
    handleDeleteContact(contact) {
      this.removeContact(contact.id);
    },
    initForm() {
      this.addContactForm.first_name = '';
      this.addContactForm.last_name = '';
      this.addContactForm.email = '';
      this.addContactForm.phone_number = '';
      this.editContactForm.id = '';
      this.editContactForm.first_name = '';
      this.editContactForm.last_name = '';
      this.editContactForm.email = '';
      this.editContactForm.phone_number = '';
      this.initialEmail = '';
    },
    removeContact(contactID) {
      const path = `http://localhost:5001/contacts/${contactID}`;
      axios.delete(path)
        .then(() => {
          this.getContacts();
          this.message = 'Contact removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getContacts();
        });
    },
    toggleAddContactModal() {
      const body = document.querySelector('body');
      this.activeAddContactModal = !this.activeAddContactModal;
      if (this.activeAddContactModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    toggleEditContactModal(contact) {
        if (contact) {
            this.initialEmail = contact.email;
            this.editContactForm = contact;
        }
        const body = document.querySelector('body');
        this.activeEditContactModal = !this.activeEditContactModal;
        if (this.activeEditContactModal) {
            body.classList.add('modal-open');
        } else{
            body.classList.remove('modal-open');
        }
    },
    toggleHistoryModal(contact) {
        if (contact) {
            this.fetchChangelog(contact);
        }
        const body = document.querySelector('body');
        this.activeHistoryModal = !this.activeHistoryModal;
        if (this.activeHistoryModal) {
            body.classList.add('modal-open');
        } else{
            body.classList.remove('modal-open');
        }
    },
    fetchChangelog(contact) {
      axios.get(`http://localhost:5001/changelog/${contact.id}`)
        .then(response => {
          this.changelog = response.data.changelog;
        })
        .catch(error => {
          console.error('Error fetching changelog:', error);
        });
    },
    handleEditCancel() {
      this.errorMessage = '';
      this.toggleEditContactModal(null);
      this.initForm();
      this.getContacts();
    },
  },
  created() {
    this.getContacts();
  },
};
</script>
