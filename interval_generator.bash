#! /bin/bash -i

FIRST_OCTAVE_NON_FLAT_NOTES=(as b)
SECOND_OCTAVE_NON_FLAT_NOTES=(c\' cs\' d\' ds\' e\' f\' fs\' g\' gs\' a\' as\' b\')
THIRD_OCTAVE_NON_FLAT_NOTES=(c\'\' cs\'\' d\'\' ds\'\' e\'\' f\'\' fs\'\' g\'\' gs\'\' a\'\' as\'\' b\'\')
FOURTH_OCTAVE_NON_FLAT_NOTES=(c\'\'\' cs\'\'\' d\'\'\' ds\'\'\' e\'\'\' f\'\'\' fs\'\'\')
NON_FLAT_NOTES=( "${FIRST_OCTAVE_NON_FLAT_NOTES[@]}" "${SECOND_OCTAVE_NON_FLAT_NOTES[@]}" "${THIRD_OCTAVE_NON_FLAT_NOTES[@]}" "${FOURTH_OCTAVE_NON_FLAT_NOTES[@]}" )

FIRST_OCTAVE_FLAT_NOTES=(bf b)
SECOND_OCTAVE_FLAT_NOTES=(c\' df\' d\' ef\' e\' f\' gf\' g\' af\' a\' bf\' b\')
THIRD_OCTAVE_FLAT_NOTES=(c\'\' df\'\' d\'\' ef\'\' e\'\' f\'\' gf\'\' g\'\' af\'\' a\'\' bf\'\' b\'\')
FOURTH_OCTAVE_FLAT_NOTES=(c\'\'\' df\'\'\' d\'\'\' ef\'\'\' e\'\'\' f\'\'\' gf\'\'\')
FLAT_NOTES=( "${FIRST_OCTAVE_FLAT_NOTES[@]}" "${SECOND_OCTAVE_FLAT_NOTES[@]}" "${THIRD_OCTAVE_FLAT_NOTES[@]}" "${FOURTH_OCTAVE_FLAT_NOTES[@]}" )

INTERVALS=(P1 m2 M2 m3 M3 P4 T P5 m6 M6 m7 M7 P8)

is_flat () {
  NOTE=$1

  echo $NOTE | grep -q '^.f'
}

generate_file_name () {
    FIRST_NOTE="$1"
    SECOND_NOTE="$2"
    INTERVAL="$3"

    echo ${FIRST_NOTE}${SECOND_NOTE}_${INTERVAL}.ly | tr "'" '-'
}

generate_score_content () {
    FIRST_NOTE="$1"
    SECOND_NOTE="$2"

    echo "\\include \"lilypond-book-preamble.ly\" \\language \"english\" { \\omit Staff.TimeSignature ${FIRST_NOTE} ${SECOND_NOTE} }"
}

generate_score_file () {
    FIRST_NOTE="$1"
    SECOND_NOTE="$2"
    INTERVAL="$3"

    generate_score_content $FIRST_NOTE $SECOND_NOTE > $(generate_file_name $FIRST_NOTE $SECOND_NOTE $INTERVAL)
}

generate_non_flat_score_files () {
    NON_FLAT_NOTES=("$@")

    NUMBER_OF_NON_FLAT_NOTES=${#NON_FLAT_NOTES[@]}

    for (( i=1; i<${NUMBER_OF_NON_FLAT_NOTES}+1; i++ ));
    do
        for (( j=1; j<${NUMBER_OF_NON_FLAT_NOTES}+1; j++ ));
        do
            if (( i <= j  && j - i <= 12 ))
            then
                FIRST_NOTE="${NON_FLAT_NOTES[$i-1]}"
                SECOND_NOTE="${NON_FLAT_NOTES[$j-1]}"
                INTERVAL="${INTERVALS[$j-$i]}"
                generate_score_file $FIRST_NOTE $SECOND_NOTE $INTERVAL
            fi
        done
    done
}

generate_flat_score_files () {
    FLAT_NOTES=("$@")

    NUMBER_OF_FLAT_NOTES=${#FLAT_NOTES[@]}

    for (( i=1; i<${NUMBER_OF_FLAT_NOTES}+1; i++ ));
    do
        for (( j=1; j<${NUMBER_OF_FLAT_NOTES}+1; j++ ));
        do
            if (( i <= j  && j - i <= 12 ))
            then
                if is_flat ${FLAT_NOTES[$i-1]} || is_flat ${FLAT_NOTES[$j-1]}
                then
                    FIRST_NOTE="${FLAT_NOTES[$i-1]}"
                    SECOND_NOTE="${FLAT_NOTES[$j-1]}"
                    INTERVAL="${INTERVALS[$j-$i]}"
                    generate_score_file $FIRST_NOTE $SECOND_NOTE $INTERVAL
                fi
            fi
        done
    done
}

generate_non_flat_score_files "${NON_FLAT_NOTES[@]}"
generate_flat_score_files "${FLAT_NOTES[@]}"
