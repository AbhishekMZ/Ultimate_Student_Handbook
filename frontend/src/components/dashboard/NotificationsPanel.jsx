import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Typography,
  Box,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  School,
  EmojiEvents,
  Notifications,
  AccessTime,
  Warning,
  Done,
} from '@mui/icons-material';

const getNotificationIcon = (type) => {
  switch (type) {
    case 'academic':
      return <School color="primary" />;
    case 'achievement':
      return <EmojiEvents color="success" />;
    case 'reminder':
      return <AccessTime color="warning" />;
    case 'alert':
      return <Warning color="error" />;
    default:
      return <Notifications color="action" />;
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
  const diffMinutes = Math.floor(diffTime / (1000 * 60));

  if (diffDays > 0) {
    return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  } else if (diffHours > 0) {
    return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  } else if (diffMinutes > 0) {
    return `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
  } else {
    return 'Just now';
  }
};

const NotificationsPanel = ({ notifications }) => {
  if (!notifications.length) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight={200}
      >
        <Typography variant="body2" color="text.secondary">
          No new notifications
        </Typography>
      </Box>
    );
  }

  return (
    <List sx={{ width: '100%', maxHeight: 400, overflow: 'auto' }}>
      {notifications.map((notification, index) => (
        <ListItem
          key={index}
          alignItems="flex-start"
          sx={{
            borderLeft: 4,
            borderLeftColor: notification.read_status ? 'transparent' : 'primary.main',
            mb: 1,
            backgroundColor: notification.read_status ? 'transparent' : 'action.hover',
            borderRadius: 1,
          }}
          secondaryAction={
            <Tooltip title="Mark as read">
              <IconButton edge="end" size="small">
                <Done />
              </IconButton>
            </Tooltip>
          }
        >
          <ListItemIcon>
            {getNotificationIcon(notification.type)}
          </ListItemIcon>
          <ListItemText
            primary={
              <Typography variant="subtitle2" component="div">
                {notification.title}
              </Typography>
            }
            secondary={
              <React.Fragment>
                <Typography
                  variant="body2"
                  color="text.primary"
                  component="div"
                  sx={{ mt: 0.5, mb: 0.5 }}
                >
                  {notification.message}
                </Typography>
                <Typography
                  variant="caption"
                  color="text.secondary"
                  component="div"
                >
                  {formatDate(notification.created_at)}
                </Typography>
              </React.Fragment>
            }
          />
        </ListItem>
      ))}
    </List>
  );
};

export default NotificationsPanel;
