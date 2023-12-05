import React from 'react'
import { Table } from 'flowbite-react';

export default function DayTable(props) {

    const dayRows = props.dayData.map((data) => (
        <Table.Row className="bg-white dark:border-gray-700 dark:bg-gray-800">
            <Table.Cell className="whitespace-nowrap font-medium text-gray-900 dark:text-white">
              {'Apple MacBook Pro 17"'}
            </Table.Cell>
            <Table.Cell>{data.day}</Table.Cell>
            <Table.Cell>{data.elevation}</Table.Cell>
            <Table.Cell>{data.runs}</Table.Cell>
          </Table.Row>
    ))


  return (
    <div className="overflow-x-auto">
      <Table hoverable>
        <Table.Head>
          <Table.HeadCell>Date</Table.HeadCell>
          <Table.HeadCell>Elevation</Table.HeadCell>
          <Table.HeadCell>Runs</Table.HeadCell>
        </Table.Head>
        <Table.Body className="divide-y">
          {dayRows}
        </Table.Body>
      </Table>
    </div>
  )
}
