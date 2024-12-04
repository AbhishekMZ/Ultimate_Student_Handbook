import { Theme } from '@mui/material';

export const styles = (theme: Theme) => ({
  root: {
    width: '100%',
    marginTop: theme.spacing(3),
    overflowX: 'auto',
  },
  table: {
    minWidth: 650,
  },
  tableHeader: {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.common.white,
  },
  tableHeaderCell: {
    color: theme.palette.common.white,
    fontWeight: 'bold',
  },
  tableRow: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
    '&:hover': {
      backgroundColor: theme.palette.action.selected,
      cursor: 'pointer',
    },
  },
});
