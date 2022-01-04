import axios from 'axios';
import React, { useEffect, useState } from "react";
import classNames from "classnames";
import { Line, Bar } from "react-chartjs-2";
import {
  Button,
  ButtonGroup,
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  CardImg,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  ButtonDropdown,
  UncontrolledDropdown,
  Label,
  FormGroup,
  Input,
  Table,
  Row,
  Col,
  UncontrolledTooltip,
} from "reactstrap";
import batsman from "assets/img/batsman.png";

function Scout(props) {
  const [bigChartData, setbigChartData] = React.useState("data1");
  const setBgChartData = (name) => {
    setbigChartData(name);
  };

  const [showBatsmanOptions, setShowBatsmanOptions] = useState(false);
  const [showBowlerOptions, setShowBowlerOptions] = useState(false);
  const [showAROptions, setShowAROptions] = useState(false);
  const [battingPosition, setBattingPosition] = useState('');
  const [minPrice, setminPrice] = useState('20l');
  const [maxPrice, setmaxPrice] = useState('2c');
  // const [cSelected, setCSelected] = useState([]);
  const [rSelected, setRSelected] = useState(null);

  function predictBatsman() {
    axios(
      // 'http://localhost/viewTicketUser', {
      ' https://b6965b5ff935.ngrok.io/predictBatsman', {
      method: 'POST',
      data: {
        "battingPosition": "topOrder",
        "minPrice": "1c",
        "maxPrice": "2c"
      },
      headers: {
        'Content-Type': 'application/json'
      }
    }
    ).then(response => {
      console.log(response.data);
    })
      .catch(error => {
        // this({ errorMessage: error.message });
        console.error('There was an error!', error);
      });

  };

  const showOptions = (e) => {
    // e.target.style.background = '#0ef086'
    setShowBatsmanOptions(true);
    setShowBowlerOptions(false);
    setShowAROptions(false);
  }

  const [dropdownOpen, setOpen] = useState(false);

  const toggle = () => setOpen(!dropdownOpen);

  return (
    <>
      <div className="content">
        <Row>
          <Col lg="8" md="12">
            <Card>
              <CardHeader outline color="secondary">
                <CardTitle tag="h2" className="text-primary">Let's find the suitable players to target in the auction</CardTitle>
              </CardHeader>
              <CardBody tag="h5" className="">
                Choose the role of the players
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col lg="4">
            <Card className="card-chart">
              <CardBody tag="h3" className="text-center">
                <Col lg="12" >
                  {/* <CardImg bottom width="100%" src="/assets/img/batsman.png" alt="Card image cap" /> */}
                  <Button
                    color="info"
                    size="md"
                    onClick={(e) => showOptions(e)}
                  >
                    Batsman
                  </Button>
                </Col>
              </CardBody>
            </Card>
          </Col>
          <Col lg="6">
            <Card className="card-chart">
              {showBatsmanOptions ?
                // <Button color="primary" size="lg">Top Order</Button>
                <div><CardBody tag="h3" className="text-center text-success">
                  <h5>Select Batsman Position</h5>
                  <ButtonGroup>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Top order</Button>
                    <Button color="info" onClick={() => setRSelected(2)} active={rSelected === 2}>Middle Order</Button>
                    <Button color="info" onClick={() => setRSelected(3)} active={rSelected === 3}>Finisher</Button>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Wicket keeper</Button>
                  </ButtonGroup>
                  <FormGroup>
                    <Label for="exampleSelect">Select</Label>
                    <Input type="select" name="select" id="exampleSelect">
                      <option>20 Lakhs</option>
                      <option>50 Lakhs</option>
                      <option>75 Lakhs</option>
                      <option>1 Crore</option>
                      <option>1.5 Crore</option>
                      <option>2 Crore</option>
                    </Input>
                  </FormGroup>
                  <FormGroup>
                    <Label for="priceRange">Minimum Price</Label>
                    <Input type="range" name="range" id="priceRange" />
                  </FormGroup>
                  <ButtonDropdown isOpen={dropdownOpen} toggle={toggle}>
                    <DropdownToggle caret color="info">
                      Select Minimum Price
                    </DropdownToggle>
                    <DropdownMenu>
                      <DropdownItem>20L</DropdownItem>
                      <DropdownItem>50L</DropdownItem>
                      <DropdownItem>75L</DropdownItem>
                      <DropdownItem>1C</DropdownItem>
                      <DropdownItem>1.5C</DropdownItem>
                      {/* <DropdownItem>2C</DropdownItem> */}
                    </DropdownMenu>
                  </ButtonDropdown>
                </CardBody>
                </div> : null}
            </Card>
          </Col>
        </Row>
        <Row>
          <Col lg="4">
            <Card className="card-chart">
              <CardBody tag="h3" className="text-center text-success">
                <Col lg="12" className="text-center text-success">
                  <Button
                    color="info"
                    size="lg"
                    onClick={() => {
                      setShowBatsmanOptions(false);
                      setShowBowlerOptions(true);
                      setShowAROptions(false);
                    }}>
                    Bowler
                  </Button>
                </Col>
              </CardBody>
            </Card>
          </Col>
          <Col lg="8">
            <Card className="card-chart">
              {showBowlerOptions ?
                // <Button color="primary" size="lg">Top Order</Button>
                <div><CardBody tag="h3" className="text-center text-success">
                  <h5>Select Batsman Position</h5>
                  <ButtonGroup>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Top order</Button>
                    <Button color="info" onClick={() => setRSelected(2)} active={rSelected === 2}>Middle Order</Button>
                    <Button color="info" onClick={() => setRSelected(3)} active={rSelected === 3}>Finisher</Button>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Wicket keeper</Button>
                  </ButtonGroup>
                </CardBody>
                </div> : null}
            </Card>
          </Col>
        </Row>
        <Row>
          <Col lg="4">
            <Card className="card-chart">
              <CardBody tag="h3" className="text-center text-success">
                <Col lg="12" className="text-center text-success">
                  <Button
                    color="info"
                    size="lg"
                    onClick={() => {
                      setShowBatsmanOptions(false);
                      setShowBowlerOptions(false);
                      setShowAROptions(true);
                    }}>
                    All Rounder
                  </Button>
                </Col>
              </CardBody>
            </Card>
          </Col>
          <Col lg="8">
            <Card className="card-chart">
              {showAROptions ?
                // <Button color="primary" size="lg">Top Order</Button>
                <div><CardBody tag="h3" className="text-center text-success">
                  <h5>Select Batsman Position</h5>
                  <ButtonGroup>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Top order</Button>
                    <Button color="info" onClick={() => setRSelected(2)} active={rSelected === 2}>Middle Order</Button>
                    <Button color="info" onClick={() => setRSelected(3)} active={rSelected === 3}>Finisher</Button>
                    <Button color="info" onClick={() => setRSelected(1)} active={rSelected === 1}>Wicket keeper</Button>
                  </ButtonGroup>
                </CardBody>
                </div> : null}
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Scout;
