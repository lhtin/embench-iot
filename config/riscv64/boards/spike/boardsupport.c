/* Copyright (C) 2012 Embecosm Limited and University of Bristol

   Contributor: Daniel Torres <dtorres@hmc.edu>

   This file is part of Embench and was formerly part of the Bristol/Embecosm
   Embedded Benchmark Suite.

   SPDX-License-Identifier: GPL-3.0-or-later */

#include <support.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

size_t start_cycle;

void
start_trigger ()
{
  asm volatile ("rdcycle %0" :"=r"(start_cycle));
}

void
stop_trigger ()
{
  size_t end_cycle;
  asm volatile ("rdcycle %0" :"=r"(end_cycle));
  printf ("Total cycle: %llu\n", end_cycle - start_cycle);
}

void
initialise_board ()
{}
