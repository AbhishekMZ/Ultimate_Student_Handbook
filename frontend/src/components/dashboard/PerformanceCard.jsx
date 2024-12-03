import React from 'react';
import {
  Box,
  Grid,
  Typography,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  TrendingUp,
  Stars,
  Warning,
  Lightbulb,
} from '@mui/icons-material';

const PerformanceCard = ({ performance }) => {
  const {
    average_score,
    completion_rate,
    strength_areas,
    weak_areas,
    improvement_rate,
    recommendations,
  } = performance;

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Scores Section */}
        <Grid item xs={12} md={6}>
          <Box mb={3}>
            <Typography variant="subtitle2" gutterBottom>
              Average Score
            </Typography>
            <Box display="flex" alignItems="center">
              <Box width="100%" mr={1}>
                <LinearProgress
                  variant="determinate"
                  value={average_score}
                  sx={{
                    height: 10,
                    borderRadius: 5,
                    backgroundColor: '#e0e0e0',
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 5,
                      backgroundColor: average_score >= 75 ? '#4caf50' : 
                                     average_score >= 60 ? '#ff9800' : '#f44336',
                    },
                  }}
                />
              </Box>
              <Box minWidth={35}>
                <Typography variant="body2" color="textSecondary">
                  {`${Math.round(average_score)}%`}
                </Typography>
              </Box>
            </Box>
          </Box>

          <Box mb={3}>
            <Typography variant="subtitle2" gutterBottom>
              Completion Rate
            </Typography>
            <Box display="flex" alignItems="center">
              <Box width="100%" mr={1}>
                <LinearProgress
                  variant="determinate"
                  value={completion_rate}
                  sx={{
                    height: 10,
                    borderRadius: 5,
                    backgroundColor: '#e0e0e0',
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 5,
                      backgroundColor: '#2196f3',
                    },
                  }}
                />
              </Box>
              <Box minWidth={35}>
                <Typography variant="body2" color="textSecondary">
                  {`${Math.round(completion_rate)}%`}
                </Typography>
              </Box>
            </Box>
          </Box>

          <Box display="flex" alignItems="center" mb={2}>
            <TrendingUp color={improvement_rate >= 0 ? "success" : "error"} />
            <Typography variant="body2" color="textSecondary" ml={1}>
              {improvement_rate >= 0 ? 'Improving' : 'Declining'} by {Math.abs(improvement_rate)}%
            </Typography>
          </Box>
        </Grid>

        {/* Strengths and Weaknesses */}
        <Grid item xs={12} md={6}>
          <Box mb={3}>
            <Typography variant="subtitle2" gutterBottom>
              Strength Areas
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {strength_areas.map((strength, index) => (
                <Chip
                  key={index}
                  icon={<Stars />}
                  label={strength}
                  color="success"
                  size="small"
                />
              ))}
            </Box>
          </Box>

          <Box mb={3}>
            <Typography variant="subtitle2" gutterBottom>
              Areas for Improvement
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {weak_areas.map((weakness, index) => (
                <Chip
                  key={index}
                  icon={<Warning />}
                  label={weakness}
                  color="warning"
                  size="small"
                />
              ))}
            </Box>
          </Box>
        </Grid>

        {/* Recommendations */}
        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            Recommendations
          </Typography>
          <List dense>
            {recommendations.map((recommendation, index) => (
              <ListItem key={index}>
                <ListItemIcon>
                  <Lightbulb color="primary" />
                </ListItemIcon>
                <ListItemText primary={recommendation} />
              </ListItem>
            ))}
          </List>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PerformanceCard;
