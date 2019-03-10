import React, { Component } from "react";
import "./App.css";
import LandingPage from "./components/landingPage/homepage";
import { Layout, Button } from "antd";
import axios from "axios";

class App extends Component {

  state = {
    userDetails: null
  }

  componentDidMount(){
    axios.defaults.baseURL = "http://localhost:8000/"
    
    const token = sessionStorage.getItem("token");
    if(token){ 
    axios.defaults.headers.common["Authorization"] = `Token ${token}`;
    }
  }

  updateUser = data => {
    console.log(data)
    const userDetails = {
      "name": data.name
    }
    this.setState({userDetails})
  } 

  handleLogout = () => {
    sessionStorage.removeItem("token")
    this.setState({userDetails: null})
  }

  render() {
    const { Header, Content, Footer} = Layout;
    const token = sessionStorage.getItem("token")
    return (
      <Layout className="layout">
        <Header style={{ background: "#fff", padding: 0, margin: 20 }}>
          <div className="logo" />
          <h1 style={{ marginLeft: 20, textAlign: "center" }}>
            Task Management Board
            {token && <Button
                type="warning"
                icon="poweroff"
                onClick={this.handleLogout}
                style={{
                  float: "right",
                  marginTop: "15px",
                  marginRight: "1%"
                }}
              >
                Logout
              </Button>
              } 
            
          </h1>
         
        </Header>

        <Content style={{ margin: 20 }}>
          <div style={{ background: "#fff", padding: 20 }}>
          {token ? 
            "Tasks" : <LandingPage updateUser={this.updateUser}/>
          }
            
          </div>
        </Content>

        <Footer style={{ textAlign: "center" }}>
          Ant Design ©2018 Created by Ant UED
        </Footer>
      </Layout>
    );
  }
}

export default App;
