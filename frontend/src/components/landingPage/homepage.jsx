import React, { Component } from "react";
import { Icon, Form, Input, Checkbox, Button, Tabs, notification } from "antd";
import axios from "axios";

const TabPane = Tabs.TabPane;

class LandingPage extends Component {
  handleLogin = e => {
    e.preventDefault();
    this.props.form.validateFields(["username", "password"], (err, values) => {
      if (!err) {
        const body = { ...values };
        const url = `accounts/local/`;
        axios.post(url, body).then(res => {
          const data = res.data;
          sessionStorage.setItem("token", data.token);
          this.props.updateUser(data);
        });
      }
    });
  };

  handleSignup = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        const body = { ...values };
        const url = `accounts/local/`;
        axios
          .put(url, body)
          .then(res => {
            const data = res.data
            sessionStorage.setItem("token", data.token);
            this.props.updateUser(data);
            notification["success"]({
              message: "User created.",
              description: res.data.message
            });
          })
          .catch(error => {
            notification["error"]({
              message: "User creation failed.",
              description: error.response.data.error
            });
          });
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <Tabs defaultActiveKey="1">
        <TabPane tab="Login" key="1">
          <Form onSubmit={this.handleLogin} className="form">
            `{" "}
            <Form.Item>
              {getFieldDecorator("username", {
                rules: [
                  { required: true, message: "Please input your username!" }
                ]
              })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: "rgba(0,0,0,.25)" }} />
                  }
                  placeholder="Username"
                  style={{width:"30%"}}
                />
              )}
            </Form.Item>
            <Form.Item>
              {getFieldDecorator("password", {
                rules: [
                  { required: true, message: "Please input your Password!" }
                ]
              })(
                <Input
                  prefix={
                    <Icon type="lock" style={{ color: "rgba(0,0,0,.25)" }} />
                  }
                  type="password"
                  placeholder="Password"
                  style={{width:"30%"}}
                />
              )}
            </Form.Item>
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                Log in
              </Button>
            </Form.Item>
          </Form>
        </TabPane>

        <TabPane tab="Sign up" key="2">
          <Form onSubmit={this.handleSignup} className="form">
            <Form.Item>
              {getFieldDecorator("username", {
                rules: [
                  { required: true, message: "Please input your username!" }
                ]
              })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: "rgba(0,0,0,.25)" }} />
                  }
                  placeholder="Username"
                  style={{width:"30%"}}
                />
              )}
            </Form.Item>

            <Form.Item>
              {getFieldDecorator("email", {
                rules: [{ required: true, message: "Please input your email!" }]
              })(
                <Input
                  prefix={
                    <Icon type="mail" style={{ color: "rgba(0,0,0,.25)" }} />
                  }
                  placeholder="Email"
                  style={{width:"30%"}}
                />
              )}
            </Form.Item>

            <Form.Item>
              {getFieldDecorator("first_name", {
                rules: [
                  { required: true, message: "Please input your First Name!" }
                ]
              })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: "rgba(0,0,0,.25)" }} />
                  }
                  placeholder="First Name"
                  style={{width:"30%"}}
                />
              )}
            </Form.Item>

            <Form.Item>
              {getFieldDecorator("last_name", {
                rules: [
                  { required: true, message: "Please input your Last Name!" }
                ]
              })(
                <Input
                  prefix={
                    <Icon type="user" style={{ color: "rgba(0,0,0,.25)" }} />
                  }
                  placeholder="Last Name"
                  style={{width:"30%"}}
                />
              )}
            </Form.Item>

            <Form.Item>
              {getFieldDecorator("password", {
                rules: [
                  { required: true, message: "Please input your Password!" }
                ]
              })(
                <Input
                  prefix={
                    <Icon type="lock" style={{ color: "rgba(0,0,0,.25)" }} />
                  }
                  type="password"
                  placeholder="Password"
                  style={{width:"30%"}}
                />
              )}
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                Sign up
              </Button>
            </Form.Item>
          </Form>
        </TabPane>
      </Tabs>
    );
  }
}

export default Form.create({ name: "form" })(LandingPage);
