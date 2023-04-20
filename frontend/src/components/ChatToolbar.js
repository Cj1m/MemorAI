import React from "react";
import { AppBar, MenuItem, Select, Toolbar, Typography } from "@mui/material";

const ChatToolbar = ({ currentInstance, setCurrentInstance }) => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          MemorAI
        </Typography>
        <Select
          value={currentInstance}
          onChange={(e) => setCurrentInstance(e.target.value)}
          displayEmpty
          inputProps={{ "aria-label": "Instance selection" }}
        >
          <MenuItem value="" disabled>
            Select an instance
          </MenuItem>
          {/* Add instances as menu items here */}
          <MenuItem value="instance1">Instance 1</MenuItem>
          <MenuItem value="instance2">Instance 2</MenuItem>
        </Select>
      </Toolbar>
    </AppBar>
  );
};

export default ChatToolbar;
