import React, { useEffect, useState } from "react";
import axios from "axios"; //npm install axios --save
import { Link } from "react-router-dom";

export default function ListUserPage() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    getUsers();
  }, []);

  async function getUsers() {
    try {
      const response = await axios.get("http://127.0.0.1:5000/get_user_details");
      console.log(response.data);
      setUsers(response.data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  }

  const deleteUser = async (id) => {
    try {
      const response = await axios.delete(`http://127.0.0.1:5000/remove_user`, { data: { id: id } });
      console.log(response.data);
      getUsers();
      alert("Successfully Deleted");
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  return (
    <div>
      <div className="container h-100">
        <div className="row h-100">
          <div className="col-12">
            <p>
              <Link to="/addnewuser" className="btn btn-success">
                Add New User
              </Link>{" "}
            </p>
            <h1>List Users</h1>
            <table class="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Date Added</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user, key) => (
                  <tr key={key}>
                    <td>{user[0]}</td>
                    <td>{user[1]}</td>
                    <td>{user[2]}</td>
                    <td>{user[3]}</td>
                    <td>
                      <Link
                        to={`user/${user[0]}/edit`}
                        className="btn btn-success"
                        style={{ marginRight: "10px" }}
                      >
                        Edit
                      </Link>
                      
                      <button
                        onClick={() => deleteUser(user[0])}
                        className="btn btn-danger"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
