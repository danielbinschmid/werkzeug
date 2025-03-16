import pandas as pd
from typing import Dict, List, Tuple


def rename_entries(df: pd.DataFrame, col: str, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Rename column entries
    """
    df[col] = df[col].map(mapping)
    return df


def dropNaNs(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Drop rows where entry of col is NaN
    """
    df_cleaned = df.dropna(subset=[col])
    return df_cleaned


def collapse_entries_with_toplevelcol(
    col: str, df: pd.DataFrame, toplevelcol: str,
) -> Tuple[pd.DataFrame, List[str]]:
    """
    @col : column to drop and collapse into toplevelcol
    @toplevelcol: target toplevelcol

    col | top_level_col | key_cols
    a | 0 | ..
    b | 1 | ..

    to 
    top_level_col_a | top_level_col_b | key_cols
    0 | 1 | ..
    """
    dfs = []

    res_df = df.copy()
    unique_vals = df[col].unique()
    for unique_val in unique_vals:
        df_val = df[df[col] == unique_val].copy().reset_index(drop=True)
        dfs.append(df_val)

        res_df[f"{toplevelcol}_{unique_val}"] = df_val[toplevelcol]

    df = dropNaNs(res_df, f"{toplevelcol}_{unique_vals[0]}")
    return res_df, [f"{toplevelcol}_{unique_val}" for unique_val in unique_vals]


def expand_col(
    df: pd.DataFrame, col: str, tgt_cols: List[str], mapping: Dict[str, List[str]]
) -> pd.DataFrame:
    """
    Expand a single column to multiple ones
    """
    df[tgt_cols] = df[col].map(mapping).apply(pd.Series)
    df = df.drop(col, axis=1)
    return df


def collapse_entries_to_subcol(
    df: pd.DataFrame, col: str, top_cols: List[str], index_cols: List[str]
) -> pd.DataFrame:
    """
    Takes a column and puts its unique value set as subcolumn of top_cols
    """
    collapsed_df = df.pivot_table(index=index_cols, columns=col, values=top_cols)

    # Reorganize columns with scores as top-level and Ac./El. as subcolumns
    collapsed_df.columns = pd.MultiIndex.from_tuples(
        [(score_type, ref_dir) for score_type, ref_dir in collapsed_df.columns]
    )

    # Reset index for clarity
    collapsed_df.reset_index(inplace=True)
    return collapsed_df


def groupBy(df: pd.DataFrame, new_key_cols: List[str]):
    """
    Groups by key cols
    """
    merged_df = df.groupby(new_key_cols).max().reset_index()
    return merged_df


def sortBy(df: pd.DataFrame, byCols: List[str]):
    """
    Sorts by byCols
    """
    sorted_df = df.sort_values(by=byCols).reset_index(drop=True)
    return sorted_df


def roundEntries(df: pd.DataFrame, n_decimals: int = 2):
    """
    Rounds entries
    """
    rounded_df = df.copy()

    # Identify numeric columns dynamically
    numeric_cols = rounded_df.select_dtypes(
        include=["float64", "float32", "int"]
    ).columns

    # Round and format in one step, removing trailing zeros
    rounded_df[numeric_cols] = rounded_df[numeric_cols].applymap(
        lambda x: f"{x:.{n_decimals}f}".rstrip("0").rstrip(".") if pd.notna(x) else ""
    )
    return rounded_df


def to_tex(df: pd.DataFrame, tex_fpath: str = "table.tex"):
    """
    Converts to tex
    """
    df.style.hide().to_latex(
        tex_fpath, multirow_align="t", multicol_align="c", siunitx=True
    )


def drop_col(df: pd.DataFrame, col: str):
    """
    drop column
    """
    df = df.drop(col, axis=1)
    return df
