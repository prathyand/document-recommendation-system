import * as React from "react";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

export default function FeedSelectFilter(props:any) {
  const [filter_value, setFilter_value] = React.useState("");


  const handleChange = (event: SelectChangeEvent) => {
    console.log(event.target.value);
    if(event.target.value=="1"){
      props.LoadFeed(false,"http://localhost:8001/feed?page=1&format=json",false,undefined,false);
    }
    if(event.target.value=="2"){
      props.LoadFeed(false,"http://localhost:8001/rediscover?page=1&format=json",false,undefined,false);
    }
    setFilter_value(event.target.value as string);
    
  };

  return (
    <Box sx={{ minWidth: 120}}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Feed</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={filter_value}
          label="filter_value"
          onChange={handleChange}
        >
          <MenuItem value={1}>New Recommendations</MenuItem>
          <MenuItem value={2}>Rediscover</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
}
