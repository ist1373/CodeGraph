// import { ReactComponent as LogoDark } from "../assets/images/logos/materialpro.svg";
import { Link } from "react-router-dom";
import logo from '../assets/images/logos/logo.png';

const Logo = () => {
  return (
    <Link to="/">
      {/* <LogoDark /> */}
      <img src={logo} alt="Company Logo" style={{ width: '300px', height: 'auto' }} />
    </Link>
  );
};

export default Logo;
