import React, { useState } from "react"

import { AppBar, Avatar, Box, Button, Container, IconButton, Link, Menu, MenuItem, Switch, Toolbar, Tooltip, Typography } from "@mui/material"
import MenuIcon from '@mui/icons-material/Menu';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import HighlightIcon from '@mui/icons-material/Highlight';
import AccountCircleRoundedIcon from '@mui/icons-material/AccountCircleRounded';
import { useUserState, useUserUpdater } from "~/contexts/UserContext";

interface HeaderProps
{
  themeChanger: React.Dispatch<React.SetStateAction<boolean>>
  isDarkTheme: boolean
}

const navMenuLinks = ['/list', '/edit-form', '/submit-form']
const pages = ['List', 'Create Form', 'Submit Form'];
const settings = ['Logout'];

const Header = (props: HeaderProps): JSX.Element =>
{
    const [anchorElNav, setAnchorElNav] = useState<null | HTMLElement>(null);
    const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);
    const user = useUserState()
    const {doUpdate} = useUserUpdater()

    const switchClicked = () => {
      const newVal = !props.isDarkTheme
      props.themeChanger(newVal)

      if (newVal)
        localStorage.setItem("isDarkTheme", "true")
      else
        localStorage.setItem("isDarkTheme", "false")
    }

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
      setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
      setAnchorElUser(event.currentTarget);
    };

    const handleCloseNavMenu = (event: React.MouseEvent<HTMLElement>) => {
      setAnchorElNav(null);
    };

    const handleCloseUserMenu = (event: React.MouseEvent<HTMLElement>) => {
      setAnchorElUser(null);
      const content = event.currentTarget.textContent
      if (content == "Logout")
        return window.open('/api/user/logout', '_self')
    };

    const loginButtonPress = () => {
      return window.open('/api/user/login', '_self')
    }

    return (
      <AppBar position="static" style={{marginBottom: "1em"}}>
        <Container>
          <Toolbar disableGutters >
            <Typography
              variant="h6"
              noWrap
              component="div"
              sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
            >
              Smart Forms
            </Typography>

            <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleOpenNavMenu}
                color="inherit"
              >
              <MenuIcon />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorElNav}
                anchorOrigin={{
                  vertical: 'bottom',
                  horizontal: 'left',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'left',
                }}
                open={Boolean(anchorElNav)}
                onClose={handleCloseNavMenu}
                sx={{
                  display: { xs: 'block', md: 'none' },
                }}
              >
                {pages.map((page) => (
                  <MenuItem key={page} onClick={handleCloseNavMenu}>
                    <Typography textAlign="center">{page}</Typography>
                  </MenuItem>
                ))}
              </Menu>
            </Box>
            <Typography
              variant="h6"
              noWrap
              component="div"
              sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
            >
              LOGO
            </Typography>



            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              {pages.map((page, i) => (
                <Button
                  key={page}
                  onClick={handleCloseNavMenu}
                  sx={{ my: 2, color: 'white', display: 'block' }}
                  href={navMenuLinks[i]}
                >
                  {page}
                </Button>
              ))}
            </Box>

            <Box sx={{ flexGrow: 0 }}>
              <MenuItem key={'switch'} sx={{p: 0}}>
                <HighlightIcon />
              </MenuItem>
            </Box>

            <Box sx={{ flexGrow: 0 }}>
              <MenuItem key={'switch'} sx={{p: 0}}>
                <Switch
                  checked={props.isDarkTheme}
                  onChange={switchClicked} />
              </MenuItem>
            </Box>

            <Box sx={{ flexGrow: 0 }}>
              <MenuItem key={'switch'} sx={{p: 0, marginRight: "2em"}}>
                <DarkModeIcon />
              </MenuItem>
            </Box>

             {/* We dont know if the user is logged in or out */}
            {user.authenticated === undefined ?

              <AccountCircleRoundedIcon sx={{ fontSize: 40 }}/> :
            // User is authenticated
            (user.authenticated && user.data ?
              <Box sx={{ flexGrow: 0 }}>
              <Tooltip title="Open settings">
                <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                  <Avatar alt={user.data.full_name} src={user.data.picture} />
                </IconButton>
              </Tooltip>
              <Menu
                sx={{ mt: '45px' }}
                id="menu-appbar"
                anchorEl={anchorElUser}
                anchorOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={Boolean(anchorElUser)}
                onClose={handleCloseUserMenu}
              >
                {settings.map((setting) => (
                  <MenuItem key={setting} onClick={handleCloseUserMenu}>
                    <Typography textAlign="center">{setting}</Typography>
                  </MenuItem>
                ))}
              </Menu>
            </Box>
            : // User is NOT authenticateed
              <Button variant="outlined" onClick={loginButtonPress}>
                Login
              </Button>
            )}


          </Toolbar>
        </Container>
      </AppBar>
    );
  };

// {/* <Switch checked={props.isDarkTheme} onChange={switchClicked} /> */}

export default Header;
